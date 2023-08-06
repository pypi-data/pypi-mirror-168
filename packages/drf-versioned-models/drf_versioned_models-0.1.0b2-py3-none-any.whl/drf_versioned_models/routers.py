"""
路由类
"""

from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter


class ModelVersionMixin:
    def __init__(self, parent_router, parent_prefix, *args, **kwargs):
        pass


class ModelVersionSimpleRouter(ModelVersionMixin, NestedSimpleRouter):
    pass
