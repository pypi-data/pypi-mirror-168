from django.urls import path, include

from rest_framework.routers import SimpleRouter
from drf_versioned_models.routers import ModelVersionSimpleRouter

from .views import CourseViewSet


app_name = 'courses'

router = SimpleRouter()
router.register(r'courses', CourseViewSet)

# version_router = ModelVersionSimpleRouter(router, r'courses', lookup='course')
# version_router.register(r'versions', CourseVersionViewSet, basename='versions')

urlpatterns = [
    path(r'', include(router.urls)),
    # path(r'', include(version_router.urls)),
]
