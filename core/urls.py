from django.urls import re_path

from core.models import Site


# serve 'view' https://github.com/wagtail/wagtail/blob/master/wagtail/core/views.py#L10
def serve(request, path):
    # Get site https://github.com/wagtail/wagtail/blob/master/wagtail/core/views.py#L12
    site = Site.objects.get(host=request.get_host())
    # Split https://github.com/wagtail/wagtail/blob/master/wagtail/core/views.py#L16
    slugs = [slug for slug in path.split("/") if slug]
    # Call page route https://github.com/wagtail/wagtail/blob/master/wagtail/core/views.py#L24
    return site.root_page.specific.route(request, slugs)


urlpatterns = [
    # Regex https://github.com/wagtail/wagtail/blob/master/wagtail/core/urls.py#L13
    # re_path https://github.com/wagtail/wagtail/blob/master/wagtail/core/urls.py#L37
    re_path(r"^((?:[\w\-]+/)*)$", serve)
]
