from jsonschema import _validators
from jsonschema.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def format_message(message):
    """
    Format error message to keep a consistent outcome
    """
    return [_(message)]


def required(validator, required, instance, schema):
    """
    Error for required field not provided
    """
    if not validator.is_type(instance, "object"):
        return
    for property in required:
        if property not in instance:
            yield ValidationError({
                property:
                format_message("This field is required.", ),
            })


def dependentRequired(validator, dependentRequired, instance, schema):
    if not validator.is_type(instance, "object"):
        return

    for property, dependency in dependentRequired.items():
        if property not in instance:
            continue

        for each in dependency:
            if each not in instance:
                message = f"{each!r} is a dependency of {property!r}"
                yield ValidationError({
                    each: format_message(message),
                })