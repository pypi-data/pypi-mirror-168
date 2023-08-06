import django

__all__ = ["action", "JSONField"]


try:
    from rest_framework.decorators import action
except ImportError:
    from rest_framework.decorators import detail_route, list_route

    def action(methods=None, detail=None, url_path=None, **kwargs):
        assert detail is not None, "@action() missing required argument: 'detail'"
        route = detail and detail_route or list_route
        return route(methods=methods, url_path=url_path, **kwargs)


if django.VERSION >= (3, 1):
    from django.db.models import JSONField
else:
    from django.contrib.postgres.fields import JSONField
