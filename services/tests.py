from django.test import TestCase

from .models import ServiceOffering


class ServiceSeoApiTests(TestCase):
    def test_services_api_exposes_public_url_and_resolved_metadata(self):
        service = ServiceOffering.objects.create(
            title="Business Website Development",
            short_description="Conversion-minded websites for growing businesses.",
            description="Expanded service description",
            active=True,
        )

        response = self.client.get("/api/services/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()[0]
        self.assertEqual(payload["seo_title"], "Business Website Development")
        self.assertEqual(
            payload["meta_description"],
            "Conversion-minded websites for growing businesses.",
        )
        self.assertTrue(payload["public_url"].endswith(f"/offerings#{service.slug}"))
