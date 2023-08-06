import logging

from django.conf import settings
from django.contrib import admin
from django.utils.module_loading import import_string

from django_perm_filter.settings import api_settings

logger = logging.getLogger(__name__)


def filter_perms(qs):
    for perm in api_settings.HIDE_PERMS:
        if "." in perm:
            app, model = perm.split(".")
            qs = qs.exclude(content_type__app_label=app, codename=model)
        else:
            qs = qs.exclude(content_type__app_label=perm)
    return qs


def unregister_models():
    if hasattr(settings, "PERM_FILTER"):
        for m in api_settings.UNREGISTER_MODELS:
            try:
                model = import_string(m)
                admin.site.unregister(model)
            except (ModuleNotFoundError, RuntimeError) as e:
                logger.warning(
                    "%s %s",
                    str(e),
                    "Ensure the module is installed and/or added to INSTALLED_APPS if need be.",
                )  # noqa
