# Django Dynamic Settings

[![Build status](https://img.shields.io/bitbucket/pipelines/akinonteam/dj-dynamic-settings)](https://bitbucket.org/akinonteam/dj-dynamic-settings/addon/pipelines/home)
![PyPI](https://img.shields.io/pypi/v/dj-dynamic-settings)
![PyPI - Django version](https://img.shields.io/pypi/djversions/dj-dynamic-settings)
![PyPI - Python version](https://img.shields.io/pypi/pyversions/dj-dynamic-settings)
![PyPI - License](https://img.shields.io/pypi/l/dj-dynamic-settings)

Django Dynamic Settings allows you to create & use dynamic settings backed by a database.

## Installation

Installation using pip:

```
pip install dj-dynamic-settings
```

`dj_dynamic_settings` app has to be added to `INSTALLED_APPS` and `migrate` command has to be run.

```python
INSTALLED_APPS = (
    # other apps here...
    "dj_dynamic_settings",
)
```

`dj_dynamic_settings.urls` must be included to a desired url path.
```python
urlpatterns = [
    ...,
    url(r"^api/v1/", include("dj_dynamic_settings.urls")),
]
```

Setting class must be defined & registered. Please make sure that this class' module 
runs whenever the application runs.
```python
from dj_dynamic_settings.registry import BaseSetting, registry
from dj_dynamic_settings.validators import TypeValidator


@registry.register
class FeatureActive(BaseSetting):
    key = "FEATURE_ACTIVE"
    validators = [TypeValidator(bool)]
    default = False
    description = "Flag for Feature X"
```

Create `Setting` instance using view.

```python
import requests

requests.post(
    url="https://your-app.com/api/v1/dynamic_settings/",
    headers={
        "Authorization": "Token <secret-login-token>",
    },
    json={
        "key": "FEATURE_ACTIVE",
        "value": True,
        "is_active": True,
    }
)
```

Access this setting as in `django.conf.settings`

```python
from dj_dynamic_settings.conf import settings


settings.FEATURE_ACTIVE  # True
```

### Create / Update Triggers

To fire a callback method when a specific setting value updated or created, you can implement `post_save_actions` in `BaseSetting` inherited class

Following example shows how to implement `post_save_actions` method.

The callback method will be called with following kwargs: 

```
key=instance.key
value=instance.value
created=created # is create operation
```

Note: `post_save_actions` returns an array, so you can add multiple callback methods. These callback methods will be called synchronously. 

```python
class PostUpdateTestConfiguration(BaseSetting):
    key = "X_FEATURE_POST_UPDATE"
    validators = [...]

    @classmethod
    def post_save_actions(cls):
        return [
            on_data_updated,
        ]

def on_data_updated(*args, **kwargs):
    pass
```


### Testing Tools

#### override_settings()

You can override a setting for a test method or test class.

```python
from dj_dynamic_settings.utils import override_settings
from django.test import TestCase

@override_settings(SOME_SETTING="some_setting")
class FeatureTestCase(TestCase):

    @override_settings(SOME_OTHER_SETTING="SOME_OTHER_SETTING")
    def test_feature(self):
        # Some stuff
        pass

    
    def test_feature_x(self):
        with override_settings(SOME_OTHER_SETTING="SOME_OTHER_SETTING"):
            # Some stuff
            pass
```
