"""

"""

from drf_versioned_models.viewsets import VersionedModelViewSet

from .models import Course
from .serializers import CourseSerializer


class CourseViewSet(VersionedModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'name'


class LectureViewSet:
    pass
