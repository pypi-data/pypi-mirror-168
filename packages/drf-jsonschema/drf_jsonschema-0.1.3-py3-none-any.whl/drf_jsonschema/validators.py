from django.utils.deconstruct import deconstructible
from jsonschema import validators
from . import _validators
from .exceptions import SchemaValidationError

# Custom validator that extends existing validator
Draft202012ValidatorExtended = validators.extend(
    validator=validators.Draft202012Validator,
    validators={
        'required': _validators.required,
        'dependentRequired': _validators.dependentRequired
    },
)


# Validate if json comply with JSONSchema
@deconstructible
class JsonSchemaFieldValidator():

    def __init__(self, schema):
        self.schema = schema

    def __call__(self, value):
        validator = Draft202012ValidatorExtended(self.schema)
        # Pass `bool` as key function to preserve original order
        error_iterator = sorted(validator.iter_errors(value), key=bool)
        error_list = self.convert_error_list(error_iterator)
        # get nested dictionary of errors message
        raise SchemaValidationError(error_list, error_iterator=error_iterator)

    def convert_error_list(self, error_list):
        # loop through error_list and store jsonschema properties name
        # with json error message as key-value pairs
        result = []
        for error in error_list:
            error_string = '"'
            error_string += error.json_path
            error_string += '": '
            if (error.validator == 'required'
                    or error.validator == 'dependentRequired'):
                for key, value in error.message.items():
                    error_string += f"'{key}'" + " " + value[0]
            else:
                error_string += error.message
            result.append(error_string)
        return result
