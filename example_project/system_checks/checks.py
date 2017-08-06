from django.core.checks import Error, register
from django.contrib.postgres.fields import ArrayField
import django.apps


@register('bug')
def example_check(app_configs, **kwargs):
    errors = []

    for model_cls in django.apps.apps.get_models():
        for field_cls in model_cls._meta.get_fields():
            if isinstance(field_cls, ArrayField) and \
                    field_cls.has_default() and not callable(field_cls.default):
                errors.append(
                    Error(
                        f"Field uses a default instance that's shared between all field instances",
                        hint="Use a callable instead, e.g., instead of `[]`, use `list`",
                        obj=field_cls,
                        id='system_checks.E001',
                    )
                )
    return errors
