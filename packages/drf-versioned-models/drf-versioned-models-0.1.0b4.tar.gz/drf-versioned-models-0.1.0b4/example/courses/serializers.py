from drf_versioned_models.serializers import VersionedModelSerializer

from .models import Course, CourseVersion


class CourseSerializer(VersionedModelSerializer):
    class Meta:
        model = Course
        exclude = ['is_active']
        version_model = CourseVersion
        version_model_fields_exclude = ['id', 'course', 'is_active']
        version_field = 'version'
        version_related_name = 'versions'
        version_field_mapping = {'created_at': 'updated_at'}
