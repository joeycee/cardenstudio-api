from urllib.parse import urljoin

from decouple import config


def get_site_url():
    configured = config("FRONTEND_SITE_URL", default="http://localhost:3000").strip()
    return configured.rstrip("/")


def absolute_site_url(path="/"):
    base = f"{get_site_url()}/"
    return urljoin(base, path.lstrip("/"))
