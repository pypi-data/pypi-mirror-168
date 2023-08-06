from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.validators import RegexValidator

setting_key_regex = r"^[A-Z]{1}[A-Z0-9_]*$"
setting_key_validator = RegexValidator(regex=setting_key_regex)


class Unset(object):
    pass


class BaseSetting(object):
    key = None
    validators = []
    default = Unset
    description = None

    @classmethod
    def post_save_actions(cls):
        return []


class SettingsRegistry(object):
    def __init__(self):
        self._registry = {}

    def register(self, cls):
        if not issubclass(cls, BaseSetting):
            raise ImproperlyConfigured(
                "Only subclasses of BaseSetting can be registered."
            )

        if cls.key in self._registry:
            raise ValueError("%s already registered." % cls.key)

        try:
            setting_key_validator(cls.key)
        except ValidationError:
            raise ImproperlyConfigured(
                "'%s' does not match regex '%s'." % (cls.key, setting_key_regex)
            )

        self._registry[cls.key] = cls
        return cls

    def keys(self):
        return self._registry.keys()

    def __getitem__(self, item):
        return self._registry[item]

    def __contains__(self, item):
        return self._registry.__contains__(item)


registry = SettingsRegistry()
