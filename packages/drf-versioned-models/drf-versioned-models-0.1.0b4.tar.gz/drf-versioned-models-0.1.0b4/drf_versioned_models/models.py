"""

"""

import uuid

from django.db import models


# ----- VersionedModel -----

class VersionedModelManager(models.Manager):
    """
    重新定义版本管理模型的增查删改行为。

    TODO：
      - 异步方法、关联模型等各种情况待验证。
    """
    def get(self, *args, **kwargs):
        """
        "获取"行为定义为获取模型主体和**可用**最新版本。

        :param args:
        :param kwargs:
        :return:
        """
        return super().get(*args, **kwargs)

    def create(self, **kwargs):
        """
        "创建"行为定义为创建不可变字段构成的模型主体和可变字段构成的它的版本。
        :return:
        """
        # 创建模型主体
        model_instance = super().create(**kwargs)
        # 创建模型版本
        model_instance.versions.create(**kwargs)
        return model_instance

    def update(self, **kwargs):
        """
        "更新"行为定义为创建可变字段构成的新版本。

        特殊情况：
        - 如果不可变字段不匹配，则抛出异常；
        - 如果可变字段不全，则拉取上一个最新版本拼接。
        :return:
        """
        # 查找模型
        model_instance = super().get(**kwargs)
        # 查找模型最新版本
        # TODO: 实际上没有get方法
        model_version_latest = model_instance.versions.get()
        # TODO：替换字段
        # 创建模型
        model_instance.versions.create(**kwargs)
        return super().update(**kwargs)


class VersionedModel(models.Model):
    """
    >>> class MyVersionedModel(VersionedModel):
    >>>     pass
    >>>
    >>> class MyModelVersion(models.Model):
    >>>     model = models.ForeignKey(MyVersionedModel, related_name='versions', on_delete=models.CASCADE, verbose_name='数据模型')

    TODO:
      - 允许直接访问ModelVersion的Field。
        比如`course.title`代替`courses.versions.latest('version').title`。
    """
    is_active = models.BooleanField(default=True, verbose_name='是否可用')

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        # TODO: 验证必填Meta
        super(VersionedModel, self).__init__(*args, **kwargs)

    def delete(self) -> None:
        """
        "删除"行为定义为`is_active`标记为`False`。

        ref:
          - https://docs.djangoproject.com/zh-hans/4.1/ref/models/instances/#deleting-objects
          - https://docs.djangoproject.com/zh-hans/4.1/topics/db/queries/#deleting-objects
          - https://docs.djangoproject.com/zh-hans/4.1/topics/db/models/#overriding-predefined-model-methods

        TODO: 返回值未设计
        """
        self.is_active = False
        super().save()


# ----- ModelVersion -----

class ModelVersionManager(models.Manager):
    def update(self):
        # TODO：临时写一下，后面优化。
        raise Exception('禁用')


class ModelVersion(models.Model):
    is_active = models.BooleanField(default=True, verbose_name='是否可用')

    class Meta:
        abstract = True

    class VersionMeta:
        """
        同上。
        """
        # 版本号字段
        version_field = 'version'
        # TODO：一组字段构成的版本号。暂不实现主要是考虑RESTful API不好定义。
        version_fields = ('version', )

    # objects = ModelVersionManager()

    def __init__(self, *args, **kwargs):
        # TODO: 验证必填Meta
        super().__init__(*args, **kwargs)

    def delete(self) -> None:
        """
        "删除"行为定义为`is_active`标记为`False`。

        ref:
          - https://docs.djangoproject.com/zh-hans/4.1/ref/models/instances/#deleting-objects
          - https://docs.djangoproject.com/zh-hans/4.1/topics/db/queries/#deleting-objects

        TODO: 返回值未设计
        """
        self.is_active = False
        super().save()
