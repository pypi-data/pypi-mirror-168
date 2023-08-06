"""
测试数据模型
"""
import uuid

from django.db import models
from drf_versioned_models.models import VersionedModel, ModelVersion


# ----- Versioned models -----

class ExampleModel(VersionedModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='ID')
    name = models.CharField(max_length=128, unique=True, verbose_name='名称')
    created_at = models.DateTimeField(verbose_name='创建时间')


class ExampleModelVersion(ModelVersion):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='版本ID')
    model = models.ForeignKey(ExampleModel, related_name='versions', on_delete=models.CASCADE, verbose_name='数据模型')
    version = models.CharField(max_length=64, verbose_name='版本')
    title = models.CharField(max_length=128, verbose_name='标题')
    created_at = models.DateTimeField(verbose_name='版本创建时间')

    class Meta:
        unique_together = ['model', 'version']


class ExampleModelVersionRelatedField(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='标签ID')
    model_version = models.ForeignKey(ExampleModelVersion, related_name='tags', on_delete=models.CASCADE, verbose_name='版本模型')
    tag = models.CharField(max_length=16, verbose_name='标签')


# ----- Nested versioned models -----

class ParentModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='ID')
    name = models.CharField(max_length=128, unique=True, verbose_name='名称')


class ParentModelVersion(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='版本ID')
    model = models.ForeignKey(ParentModel, related_name='versions', on_delete=models.CASCADE, verbose_name='数据模型')
    title = models.CharField(max_length=128, verbose_name='标题')


class ChildModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='ID')
    name = models.CharField(max_length=128, unique=True, verbose_name='名称')
    parent = models.ForeignKey(ParentModel, related_name='children', on_delete=models.CASCADE, verbose_name='父模型')


class ChildModelVersion(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='版本ID')
    parent = models.ForeignKey(ParentModelVersion, related_name='children', on_delete=models.CASCADE, verbose_name='父模型')
    model = models.ForeignKey(ChildModel, related_name='versions', on_delete=models.CASCADE, verbose_name='数据模型')
    title = models.CharField(max_length=128, verbose_name='标题')


# ----- Multi versioned models -----

class MultiVersionedModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='ID')
    name = models.CharField(max_length=128, unique=True, verbose_name='名称')


class Part1ModelVersion(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='ID')
    title = models.CharField(max_length=128, verbose_name='标题')


class Part2ModelVersion(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, verbose_name='ID')
    description = models.CharField(max_length=128, verbose_name='描述')
