from django.db import models
import json
from drf_jsonschema.validators import JsonSchemaFieldValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_even(self):
    if 3 % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': 3},
        )


def validate_odd(self):
    if 4 % 2 == 0:
        raise ValidationError(
            _('%(value)s is not an odd number'),
            params={'value': 4},
        )


class ModelWithJsonField(models.Model):
    with open('drf_jsonschema/tests/schemas/test_schema.json') as file:
        test_jsonschema = json.load(file)
    json_data = models.JSONField(validators=[
        JsonSchemaFieldValidator(
            schema=test_jsonschema), validate_even, validate_odd
    ])
