from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from tests.serializers import SchemaSerializer


# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def test_api_view(request):
    json_schema_data = {
        "name":
        1,
        "test_uniqueItems": [1, 2, 3, 4, 4],
        "test_tupleValidation": [24, "Sussex"],
        "test_unevaluatedItems":
        ["life", "universe", "everything", "forty-two"],
        "test_exclusiveMaximum":
        99,
        "test_regex":
        "(888)555-1212 ext. 532",
        "test_integer":
        1,
        "test_additionalProperties":
        "hello",
        "test_minimumProperties": {
            "a": 0
        },
        "children": [{
            "name": "johnny",
            "test_additionalItems": "1"
        }, {
            "children": [{
                "test_uniqueItems": [1, 2, 3],
                "test_additionalItems":
                "1",
                "children": [{
                    "name": "john",
                    "test_uniqueItems": [1, 2, 3],
                    "test_exclusiveMaximum": 99
                }]
            }]
        }]
    }

    serializer = SchemaSerializer(data={"json_data": json_schema_data})
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
