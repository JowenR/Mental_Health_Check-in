from django.urls import reverse, NoReverseMatch
from .data.sidebar import SIDEBAR_LINKS


def sidebar_data(request):
    current = getattr(request.resolver_match, "url_name", None)
    links = []
    for link in SIDEBAR_LINKS:
        try:
            href = reverse(link["url_name"])
        except NoReverseMatch:  # page doesn't exist yet
            href = "#"
        links.append({**link, "href": href, "active": link["url_name"] == current})
    return {"sidebar_links": links}