from django.http import HttpResponse
from django.utils import timezone

from blog.models import BlogPost
from portfolio.models import PortfolioProject
from services.models import ServiceOffering

from .seo import absolute_site_url


def robots_txt(_request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /api/",
        "Disallow: /tinymce/",
        f"Sitemap: {absolute_site_url('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(_request):
    now = timezone.now().date().isoformat()

    urls = [
        {"loc": absolute_site_url("/"), "lastmod": now},
        {"loc": absolute_site_url("/about"), "lastmod": now},
        {"loc": absolute_site_url("/offerings"), "lastmod": now},
        {"loc": absolute_site_url("/work"), "lastmod": now},
        {"loc": absolute_site_url("/blog"), "lastmod": now},
        {"loc": absolute_site_url("/testimonials"), "lastmod": now},
        {"loc": absolute_site_url("/contact"), "lastmod": now},
    ]

    urls.extend(
        {
            "loc": absolute_site_url(f"/blog/{post.slug}"),
            "lastmod": (post.updated_at or post.published_at or post.created_at).date().isoformat(),
        }
        for post in BlogPost.objects.filter(published=True)
    )
    urls.extend(
        {
            "loc": absolute_site_url(f"/work/{project.slug}"),
            "lastmod": (project.updated_at or project.created_at).date().isoformat(),
        }
        for project in PortfolioProject.objects.filter(active=True)
    )
    urls.extend(
        {
            "loc": absolute_site_url("/offerings"),
            "lastmod": (service.updated_at or service.created_at).date().isoformat(),
        }
        for service in ServiceOffering.objects.filter(active=True)
    )

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for entry in urls:
        xml_lines.extend(
            [
                "  <url>",
                f"    <loc>{entry['loc']}</loc>",
                f"    <lastmod>{entry['lastmod']}</lastmod>",
                "  </url>",
            ]
        )
    xml_lines.append("</urlset>")

    return HttpResponse("\n".join(xml_lines), content_type="application/xml")
