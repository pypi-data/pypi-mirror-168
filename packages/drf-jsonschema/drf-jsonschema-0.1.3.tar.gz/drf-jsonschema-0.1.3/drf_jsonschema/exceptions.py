from django.core.exceptions import ValidationError


# Custom class to validate schema
class SchemaValidationError(ValidationError):

    def __init__(self, message, code=None, params=None, error_iterator=None):
        super().__init__(message, code, params)
        self.error_iterator = error_iterator
