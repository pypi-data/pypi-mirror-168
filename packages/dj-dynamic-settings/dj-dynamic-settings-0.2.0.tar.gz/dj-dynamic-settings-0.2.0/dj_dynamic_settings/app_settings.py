from django.conf import settings
from django.core.cache import DEFAULT_CACHE_ALIAS

__all__ = ["app_settings"]


defaults = {
    "CACHE_KEY_PREFIX": "dynamic-settings",
    "CACHE_ALIAS": DEFAULT_CACHE_ALIAS,
    "USE_CACHE": True,
    "CACHE_TIMEOUT": 1 * 60 * 60,
}


class AppSettings(object):
    def __init__(self, prefix):
        self._prefix = prefix

    def __getattr__(self, key):
        if key not in defaults:
            raise AttributeError(
                "'{0}' object has no attribute '{1}'".format(
                    self.__class__.__name__, key
                )
            )

        setting_key = "{0}{1}".format(self._prefix, key)
        return getattr(settings, setting_key, defaults[key])


app_settings = AppSettings("DYNAMIC_SETTINGS_")
