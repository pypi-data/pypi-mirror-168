from rest_framework import serializers

from dj_dynamic_settings.registry import BaseSetting, registry
from dj_dynamic_settings.validators import SerializerValidator, TypeValidator


class FeatureConfigurationSerializer(serializers.Serializer):
    value_a = serializers.BooleanField()
    value_b = serializers.FloatField()


class FeatureRuleSerializer(serializers.Serializer):
    value_c = serializers.BooleanField()
    value_d = serializers.FloatField()
    value_e = serializers.CharField()


@registry.register
class FeatureActive(BaseSetting):
    key = "X_FEATURE_ACTIVE"
    validators = [TypeValidator(bool)]


@registry.register
class DefaultFeatureActive(BaseSetting):
    key = "Y_FEATURE_ACTIVE"
    validators = [TypeValidator(bool)]
    default = True


@registry.register
class TrialCount(BaseSetting):
    key = "X_TRIAL_COUNT"
    validators = [TypeValidator(int)]


@registry.register
class FeatureConfiguration(BaseSetting):
    key = "X_FEATURE_CONFIGURATION"
    validators = [SerializerValidator(FeatureConfigurationSerializer)]


@registry.register
class FeatureRulesConfiguration(BaseSetting):
    key = "X_FEATURE_RULES"
    validators = [
        SerializerValidator(FeatureRuleSerializer, serializer_kwargs={"many": True})
    ]


@registry.register
class FeatureConfigurationWithDefaultValue(BaseSetting):
    key = "X_FEATURE_CONFIGURATION_WITH_DEFAULT_VALUE"
    validators = [TypeValidator(str)]
    default = "default_value"


@registry.register
class PostUpdateTestConfiguration(BaseSetting):
    key = "X_FEATURE_POST_UPDATE"
    validators = [SerializerValidator(FeatureConfigurationSerializer)]

    @classmethod
    def post_save_actions(cls):
        return [
            on_data_updated,
        ]


def on_data_updated(*args, **kwargs):
    pass
