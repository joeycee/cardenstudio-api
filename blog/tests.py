from django.test import TestCase, override_settings

from .models import BlogPost


class BlogSeoApiTests(TestCase):
    @override_settings(ALLOWED_HOSTS=["testserver"])
    def test_blog_api_exposes_seo_fields_and_public_url(self):
        post = BlogPost.objects.create(
            title="SEO foundations for premium websites",
            seo_title="SEO Foundations",
            meta_description="Practical SEO guidance for a premium website launch.",
            excerpt="Short summary",
            content="Long form article",
            published=True,
        )

        response = self.client.get("/api/blog/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()[0]
        self.assertEqual(payload["slug"], post.slug)
        self.assertEqual(payload["seo_title"], "SEO Foundations")
        self.assertEqual(
            payload["meta_description"],
            "Practical SEO guidance for a premium website launch.",
        )
        self.assertTrue(payload["public_url"].endswith(f"/blog/{post.slug}"))

    @override_settings(ALLOWED_HOSTS=["testserver"])
    def test_sitemap_and_robots_reference_public_routes(self):
        post = BlogPost.objects.create(
            title="Search visibility checklist",
            excerpt="Short summary",
            content="Long form article",
            published=True,
        )

        robots_response = self.client.get("/robots.txt")
        sitemap_response = self.client.get("/sitemap.xml")

        self.assertEqual(robots_response.status_code, 200)
        self.assertContains(robots_response, "Disallow: /api/")
        self.assertContains(robots_response, "Sitemap: http://localhost:3000/sitemap.xml")
        self.assertEqual(sitemap_response.status_code, 200)
        self.assertContains(sitemap_response, "<loc>http://localhost:3000/blog</loc>")
        self.assertContains(sitemap_response, f"<loc>http://localhost:3000/blog/{post.slug}</loc>")
