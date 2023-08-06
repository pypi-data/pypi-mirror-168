from django.urls import path, include

from rest_framework_nested.routers import SimpleRouter
from drf_versioned_models.routers import ModelVersionSimpleRouter

from .views import ExampleModelViewSet


app_name = 'tests'


router = SimpleRouter()
router.register(r'examples', ExampleModelViewSet)

# version_router = ModelVersionSimpleRouter(router, r'courses', lookup='course')
# version_router.register(r'versions', ExampleModelVersionSerializer, basename='versions')

urlpatterns = [
    path(r'', include(router.urls)),
    # path(r'', include(version_router.urls)),
]
