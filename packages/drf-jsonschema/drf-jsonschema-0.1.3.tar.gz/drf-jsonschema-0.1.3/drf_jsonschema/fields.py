from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.fields import JSONField
from .exceptions import SchemaValidationError
from .validators import JsonSchemaFieldValidator


class JSONSchemaField(JSONField):

    def __init__(self, *args, **kwargs):
        self.schema = kwargs.pop('schema', None)
        super().__init__(*args, **kwargs)

    def run_validators(self, value):
        error_list = None
        schema_validator = None

        # Find JsonSchemaFieldValidator and removed it
        # This is to prevent DRFValidationError raised before
        # SchemaValidationError is caught.
        # The JsonSchemaFieldValidator will be called and run manually
        # after other validators are run.
        for validator in self.validators:
            if isinstance(validator, JsonSchemaFieldValidator):
                schema_validator = validator
                # Remove JsonSchemaFieldValidator to prevent running twice
                self.validators.remove(validator)

        try:
            # Run other validators except for JsonSchemaFieldValidator
            super().run_validators(value)

        # Update error_dictionary with the error if rest_framework
        # validation_error is raised
        except DRFValidationError as e:
            error_list = e.detail

        try:
            # Instantiate JsonSchemaFieldValidator if the validator
            # is not found
            if not schema_validator:
                # Raise Exception if json schema is not found
                if not self.schema or self.schema is None:
                    raise ValueError("Missing json schema")
                schema_validator = JsonSchemaFieldValidator(self.schema)

            # Run our schema validator manually
            schema_validator(value)

            if error_list:
                raise DRFValidationError(error_list)

        except SchemaValidationError as e:
            # Construct the error dictionary if SchemaValidationError is raised
            error_tree = self.construct_error_dictionary(e.error_iterator)

            if error_list:
                errors = self._get_error_list(error_tree)
                # Append DRFValidation error messages if found
                for error_message in error_list:
                    errors.append(error_message)

            raise DRFValidationError(error_tree)

    # Return a dictionary of errors.
    def construct_error_dictionary(self, error_iterator: dict):
        result = {}
        for error in error_iterator:
            nested = result

            # Append error message if path is empty and error message is string
            if not error.absolute_path and not isinstance(error.message, dict):
                errors = self._get_error_list(nested)
                errors.append(error.message)
                continue
            elif not error.absolute_path and isinstance(error.message, dict):
                errors = self._append_error_message(error.message, nested)
                continue
            last_index = len(error.absolute_path) - 1

            for index, step in enumerate(error.absolute_path):
                # Create nested structure if index not last
                nested = self._get_or_create_nested_dict(nested, step)

                # Append error message if it is last index
                if index == last_index:

                    # Append error message if message is string
                    if not isinstance(error.message, dict):
                        errors = self._get_error_list(nested)
                        errors.append(error.message)
                    # Pass error.message (dict) to the method for structuring
                    # error message
                    else:
                        errors = self._append_error_message(
                            error.message, nested)
        return result

    def _get_or_create_nested_dict(self, obj: dict, key: str):
        value = obj.get(key, {})
        obj[key] = value
        return value

    def _get_error_list(self, obj: dict):
        value = obj.get('errors', [])
        obj['errors'] = value
        return value

    def _append_error_message(self, error: dict, nested: dict):
        # Loop through error.message (dict) to append error message
        for key, error_message in error.items():
            nested = self._get_or_create_nested_dict(nested, key)
            errors = self._get_error_list(nested)
            errors.append(error_message[0])
        return errors
