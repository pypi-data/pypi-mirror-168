from drf_versioned_models.viewsets import VersionedModelViewSet

from .models import ExampleModel
from .serializers import ExampleModelSerializer


class ExampleModelViewSet(VersionedModelViewSet):
    queryset = ExampleModel.objects.all()
    serializer_class = ExampleModelSerializer
    lookup_field = 'name'


class LectureViewSet:
    pass
