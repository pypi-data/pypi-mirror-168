from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete, post_save

from dj_dynamic_settings.app_settings import app_settings
from dj_dynamic_settings.compat import JSONField
from dj_dynamic_settings.conf import delete_setting_from_cache, run_post_save_actions
from dj_dynamic_settings.registry import registry


def registry_contains_validator(value):
    if value not in registry.keys():
        raise ValidationError('"%s" is not a valid choice.' % value)


class Setting(models.Model):
    key = models.CharField(
        max_length=128,
        validators=[registry_contains_validator],
        unique=True,
    )
    value = JSONField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s = %s" % (self.key, self.value)


if app_settings.USE_CACHE:
    post_save.connect(delete_setting_from_cache, sender=Setting)
    post_delete.connect(delete_setting_from_cache, sender=Setting)

post_save.connect(run_post_save_actions, sender=Setting)
