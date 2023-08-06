from django import template
from django.urls import reverse

from obpages.templatetags.constants import OBPAGES_COMPONENTS_PATH

OBPAGES_LINKS_PATH = f"{OBPAGES_COMPONENTS_PATH}/links"

register = template.Library()


@register.inclusion_tag(f"{OBPAGES_LINKS_PATH}/nav_link.html")
def nav_link(request, name, title):
    url = reverse(viewname=name)
    try:
        current = url == request.path
    except AttributeError:
        # request has no path attribute; likely a server error
        current = False
    return {"url": reverse(viewname=name), "title": title, "current": current}


@register.inclusion_tag(f"{OBPAGES_LINKS_PATH}/site_link.html")
def site_link(item):
    return {"item": item}


@register.inclusion_tag(f"{OBPAGES_LINKS_PATH}/content_link.html")
def content_link(item, is_staff=False):
    admin_url = reverse(
        f"admin:{item._meta.app_label}_{item._meta.model_name}_change", args=(item.pk,)
    )
    return {"item": item, "is_staff": is_staff, "admin_url": admin_url}


@register.inclusion_tag(f"{OBPAGES_LINKS_PATH}/classifier_link.html")
def classifier_link(item):
    return {"item": item}


@register.inclusion_tag(f"{OBPAGES_LINKS_PATH}/sequence_link.html")
def sequence_link(sequence):
    return {"sequence": sequence}
