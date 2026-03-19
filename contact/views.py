import json
from html import escape
from urllib import error, parse, request

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer


class ContactDeliveryError(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = 'Your message was saved, but we could not deliver the email notification.'
    default_code = 'contact_delivery_failed'


class RecaptchaVerificationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'reCAPTCHA verification failed. Please try again.'
    default_code = 'recaptcha_verification_failed'


class ContactSubmissionCreateView(CreateAPIView):
    queryset = ContactSubmission.objects.all()
    serializer_class = ContactSubmissionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recaptcha_token = serializer.validated_data.pop('recaptcha_token')

        self.verify_recaptcha(recaptcha_token, request)
        submission = serializer.save()

        response_data = dict(serializer.data)
        response_data['notification_delivered'] = True

        try:
            self.send_notification_email(submission)
        except ContactDeliveryError as exc:
            response_data['notification_delivered'] = False
            response_data['detail'] = str(exc.detail)

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def verify_recaptcha(self, token, incoming_request):
        if not settings.RECAPTCHA_SECRET_KEY:
            if settings.DEBUG:
                return
            raise RecaptchaVerificationError('reCAPTCHA is not configured on the server.')

        remote_ip = self.get_client_ip(incoming_request)
        payload = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': token,
        }
        if remote_ip:
            payload['remoteip'] = remote_ip

        req = request.Request(
            settings.RECAPTCHA_VERIFY_URL,
            data=parse.urlencode(payload).encode('utf-8'),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            method='POST',
        )

        try:
            with request.urlopen(req, timeout=settings.CONTACT_FORM_API_TIMEOUT) as response:
                body = json.loads(response.read().decode('utf-8'))
        except error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='replace')
            raise RecaptchaVerificationError(
                f'reCAPTCHA verification failed due to a provider error: {detail}'
            ) from exc
        except error.URLError as exc:
            raise RecaptchaVerificationError(
                'reCAPTCHA could not be verified right now. Please try again.'
            ) from exc

        if not body.get('success'):
            error_codes = body.get('error-codes') or []
            if error_codes:
                raise RecaptchaVerificationError(
                    f"reCAPTCHA verification failed: {', '.join(error_codes)}"
                )
            raise RecaptchaVerificationError()

    def get_client_ip(self, incoming_request):
        forwarded_for = incoming_request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        return incoming_request.META.get('REMOTE_ADDR', '')

    def send_notification_email(self, submission):
        if not settings.SMTP2GO_API_KEY:
            raise ContactDeliveryError('SMTP2GO is not configured on the server.')

        if not settings.CONTACT_FORM_TO_EMAIL:
            raise ContactDeliveryError('The contact form recipient email is not configured on the server.')

        reply_to = settings.CONTACT_FORM_REPLY_TO or submission.email
        payload = {
            'api_key': settings.SMTP2GO_API_KEY,
            'to': [settings.CONTACT_FORM_TO_EMAIL],
            'sender': f"{settings.CONTACT_FORM_FROM_NAME} <{settings.CONTACT_FORM_FROM_EMAIL}>",
            'subject': f"{settings.CONTACT_FORM_SUBJECT_PREFIX}: {submission.name}",
            'text_body': self.build_text_body(submission),
            'html_body': self.build_html_body(submission),
            'custom_headers': [
                {
                    'header': 'Reply-To',
                    'value': reply_to,
                }
            ],
        }

        req = request.Request(
            'https://api.smtp2go.com/v3/email/send',
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST',
        )

        try:
            with request.urlopen(req, timeout=settings.CONTACT_FORM_API_TIMEOUT) as response:
                body = json.loads(response.read().decode('utf-8'))
        except error.HTTPError as exc:
            detail = exc.read().decode('utf-8', errors='replace')
            raise ContactDeliveryError(
                f'Your message was saved, but SMTP2GO rejected the email notification: {detail}'
            ) from exc
        except error.URLError as exc:
            raise ContactDeliveryError from exc

        if body.get('data', {}).get('succeeded', 0) < 1:
            raise ContactDeliveryError(
                f"Your message was saved, but SMTP2GO did not confirm delivery: {body.get('data') or body}"
            )

    def build_text_body(self, submission):
        return (
            "New contact form enquiry\n\n"
            f"Name: {submission.name}\n"
            f"Email: {submission.email}\n"
            f"Business Name: {submission.business_name or '-'}\n"
            f"Project Type: {submission.project_type}\n"
            f"Budget Range: {submission.budget_range or '-'}\n"
            f"Timeline: {submission.timeline or '-'}\n"
            f"Submitted At: {submission.created_at.isoformat()}\n\n"
            "Message:\n"
            f"{submission.message}\n"
        )

    def build_html_body(self, submission):
        message_html = escape(submission.message).replace('\n', '<br>')
        return (
            "<h2>New contact form enquiry</h2>"
            f"<p><strong>Name:</strong> {escape(submission.name)}</p>"
            f"<p><strong>Email:</strong> {escape(submission.email)}</p>"
            f"<p><strong>Business Name:</strong> {escape(submission.business_name or '-')}</p>"
            f"<p><strong>Project Type:</strong> {escape(submission.project_type)}</p>"
            f"<p><strong>Budget Range:</strong> {escape(submission.budget_range or '-')}</p>"
            f"<p><strong>Timeline:</strong> {escape(submission.timeline or '-')}</p>"
            f"<p><strong>Submitted At:</strong> {submission.created_at.isoformat()}</p>"
            f"<p><strong>Message:</strong></p><p>{message_html}</p>"
        )
