from drf_jsonschema.serializers import JsonSchemaModelSerializer
from tests.models import ModelWithJsonField


class SchemaSerializer(JsonSchemaModelSerializer):

    class Meta:
        model = ModelWithJsonField
        fields = '__all__'
