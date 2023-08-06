from rest_framework import serializers

from drf_versioned_models.serializers import VersionedModelSerializer

from .models import *


class ExampleModelSerializer(VersionedModelSerializer):
    class Meta:
        model = ExampleModel
        exclude = ['is_active']
        version_model = ExampleModelVersion
        version_model_fields_exclude = ['id', 'model', 'is_active']
        version_field_mapping = {'created_at': 'updated_at'}
