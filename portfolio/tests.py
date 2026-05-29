from django.test import TestCase

from .models import PortfolioProject


class PortfolioSeoApiTests(TestCase):
    def test_portfolio_api_uses_seo_fallbacks(self):
        project = PortfolioProject.objects.create(
            title="Studio Redesign",
            short_description="Sharper positioning for a service business.",
            full_description="Detailed case study body",
            active=True,
        )

        response = self.client.get("/api/portfolio/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()[0]
        self.assertEqual(payload["seo_title"], "Studio Redesign")
        self.assertEqual(
            payload["meta_description"],
            "Sharper positioning for a service business.",
        )
        self.assertTrue(payload["public_url"].endswith(f"/work/{project.slug}"))
