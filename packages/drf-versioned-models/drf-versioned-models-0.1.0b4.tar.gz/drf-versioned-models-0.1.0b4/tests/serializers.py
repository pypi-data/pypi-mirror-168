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


class ExampleModelVersionSerializer(serializers.ModelSerializer):
    # https://www.django-rest-framework.org/api-guide/relations/#slugrelatedfield
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='tag')

    class Meta:
        model = ExampleModelVersion
        exclude = ['id', 'model', 'is_active']

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret['tags'] = data['tags']
        return ret

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        instance = super().create(validated_data)
        for tag in tags:
            instance.tags.create(tag=tag)
        return instance


class ExampleModelWithTagSerializer(VersionedModelSerializer):

    class Meta:
        model = ExampleModel
        exclude = ['is_active']
        version_serializer = ExampleModelVersionSerializer
        version_field_mapping = {'created_at': 'updated_at'}
