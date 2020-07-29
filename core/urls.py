from django.urls import re_path

from core.models import Site


def serve(request, path):
    site = Site.objects.get(host=request.get_host())
    slugs = [slug for slug in path.split("/") if slug]
    return site.root_page.specific.route(request, slugs)


urlpatterns = [
    re_path(r"^((?:[\w\-]+/)*)$", serve)
]
