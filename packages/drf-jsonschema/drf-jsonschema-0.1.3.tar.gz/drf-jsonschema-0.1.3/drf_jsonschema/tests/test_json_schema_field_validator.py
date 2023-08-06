from django.test import TestCase
from drf_jsonschema.validators import (Draft202012ValidatorExtended,
                                   JsonSchemaFieldValidator)


# Create your tests here.
class Test(TestCase):
    """
    Test on JsonSchemaFieldValidator
    """

    def test_convert_error_list_path(self):
        """
        Return false if path is not correcly formed
        """
        test_schema = {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string"
                },
                "gender": {
                    "type": "string"
                },
                "children": {
                    "type": "array",
                    "items": {
                        "$ref": "#"
                    }
                }
            },
            "required": ["gender"]
        }
        test_json = {
            "name":
            "Elizabeth",
            "gender":
            "female",
            "children": [{
                "name":
                "Charles",
                "gender":
                "male",
                "children": [{
                    "name":
                    "William",
                    "gender":
                    "male",
                    "children": [{
                        "name": 1,
                        "gender": "female"
                    }, {
                        "name": "Charlotte",
                        "gender": "female"
                    }]
                }, {
                    "name": "Harry",
                    "gender": "male"
                }]
            }]
        }
        validator = Draft202012ValidatorExtended(test_schema)
        error_list = sorted(validator.iter_errors(test_json), key=bool)
        error_list = JsonSchemaFieldValidator.convert_error_list(
            self, error_list)
        self.assertEqual(error_list, [
            '"$.children[0].children[0].children[0].name": 1 is not of type \'string\''
        ])
