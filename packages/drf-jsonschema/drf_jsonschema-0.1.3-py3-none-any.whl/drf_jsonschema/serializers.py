from rest_framework import serializers
from drf_jsonschema.fields import JSONSchemaField
from django.db import models


class JsonSchemaModelSerializer(serializers.ModelSerializer):
    serializer_field_mapping = serializers.ModelSerializer\
        .serializer_field_mapping.copy()
    serializer_field_mapping[models.JSONField] = JSONSchemaField
