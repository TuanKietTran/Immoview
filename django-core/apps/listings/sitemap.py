from django.http import HttpResponse
from django.utils.html import conditional_escape

from .infrastructure.models import ListingModel


def sitemap(request):
    rows = ListingModel.objects.filter(status="published").exclude(slug="").values_list("slug", flat=True)[:5000]
    urls = "".join(f"<url><loc>{conditional_escape(request.build_absolute_uri('/listings/' + slug + '/'))}</loc></url>" for slug in rows)
    body = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return HttpResponse(body, content_type="application/xml")
