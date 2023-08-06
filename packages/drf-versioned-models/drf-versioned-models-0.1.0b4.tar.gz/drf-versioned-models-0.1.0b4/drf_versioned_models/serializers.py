# -*- coding: utf-8 -*-

from rest_framework import serializers


class VersionedModelSerializer(serializers.ModelSerializer):
    """
    版本化模型序列化类

    假设被序列化的模型由`Model`和`ModelVersion`的最新版本组成。
    其中`Model`定义不可变字段，`ModelVersion`定义可变字段。

    ```python
    class CourseSerializer(VersionedModelSerializer):
        class Meta:
            version_model = CourseVersion
            version_model_fields_exclude = ['id', 'is_active', 'course']
            version_field = 'version'
            version_related_name = 'versions'
            version_field_mapping = {
                'created_at': 'updated_at'
            }
    ```
    """

    # ----- 初始化 -----

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 版本相关Meta设置
        self._init_version_meta()
        # 验证
        # 版本字段冲突抛出异常，让开发者自己处理
        self._validate_duplicate_fields()
        # partial_update定义为上个版本基础上update字段以后更新
        if self.partial:
            self.initial_data = self._get_partial_update_initial_data(self.initial_data)

    def _init_version_meta(self):
        # 常用Meta设置
        self._model_class = self.Meta.model
        self._model_class_name = self._model_class.__name__
        # 版本序列化类
        self._version_serializer_class = getattr(self.Meta, 'version_serializer', None)
        # 版本模型类
        self._version_model_class = getattr(self.Meta, 'version_model', None) or self._version_serializer_class.Meta.model
        # 版本序列化字段
        # TODO: 给版本序列化类时需要修改
        self._version_model_fields_exclude = getattr(self.Meta, 'version_model_fields_exclude', ['id', 'is_active'])
        # 版本标记字段，默认为`version`
        self._version_field = getattr(self.Meta, 'version_field', 'version')
        # 版本关联字段，默认为`versions`
        self._version_related_name = getattr(self.Meta, 'version_related_name', 'versions')
        # 版本外键字段
        self._version_foreign_key_field_name = getattr(self._model_class, self._version_related_name).field.name
        # 序列化行为版本字段匹配表，默认为空
        self._version_field_mapping = self._validate_version_field_mapping(getattr(self.Meta, 'version_field_mapping', {}))
        # 反序列行为版本字段匹配表，默认为空
        self._version_field_mapping_reverse = {value: key for key, value in getattr(self.Meta, 'version_field_mapping', {}).items()}

    def _validate_version_field_mapping(self, version_field_mapping):
        """
        TODO:
          - 待转字段必须存在
          - key和value不能一样，否则没意义，还影响后面的验证逻辑。

        :param version_field_mapping:
        :return:
        """
        return version_field_mapping

    def get_default_version_serializer_class(self):
        return type(f"{self._model_class_name}Serializer", (serializers.ModelSerializer, ), {
            "Meta": type("Meta", (object,), {
                "model": self._version_model_class,
                "exclude": self._version_model_fields_exclude,
            })
        })

    @property
    def version_serializer_class(self):
        return self._version_serializer_class or self.get_default_version_serializer_class()

    def _validate_duplicate_fields(self):
        """
        TODO:
          - bugfix: 结合mapping表。
          - 增加重复字段提示。
        :return:
        """
        # 模型字段
        model_fields = self.get_fields().keys()
        # 模型版本字段
        model_version_fields = self.version_serializer_class().get_fields().keys()
        # 重复字段
        duplicated_fields = set(model_fields) & set(model_version_fields) - set(self._version_field_mapping.keys())
        if duplicated_fields:
            raise serializers.ValidationError("未处理重复字段")

    def _get_partial_update_initial_data(self, initial_data: dict) -> dict:
        data = self.to_representation(self.instance)
        data.update(initial_data)
        return data

    # ----- 序列化 -----

    def to_representation(self, instance) -> dict:
        """
        :param instance:
        :return:
        """
        instance_latest_version = instance.versions.latest(self._version_field)
        ret = super().to_representation(instance)
        ret_version = self.version_serializer_class().to_representation(instance_latest_version)
        # 处理版本字段名称更变，比如版本`created_at`改为`updated_at`
        ret_version = self._replace_version_field(ret_version)
        ret.update(ret_version)
        return ret

    def _replace_version_field(self, data):
        new_data = {}
        for key in data:
            if key in self._version_field_mapping:
                new_data[self._version_field_mapping[key]] = data[key]
            else:
                new_data[key] = data[key]
        return new_data

    # ----- 反序列化 -----

    def to_internal_value(self, data):
        # 主模型
        model_data = super().to_internal_value(data)
        # 版本模型
        version_data = self._filter_version_data(data, model_data)
        version_data = self.version_serializer_class().to_internal_value(version_data)
        model_data[self._version_related_name] = [version_data]
        return model_data

    def _filter_version_data(self, data, model_data):
        version_data = {}
        for key in data:
            if key not in model_data:
                if key in self._version_field_mapping_reverse:
                    version_data[self._version_field_mapping_reverse[key]] = data[key]
                else:
                    version_data[key] = data[key]
        return version_data

    def create_version(self, instance, version_validated_data):
        version_validated_data.update({self._version_foreign_key_field_name: instance})
        serializer = self.version_serializer_class(data=version_validated_data)
        if serializer.is_valid(raise_exception=True):
            version_instance = serializer.create(version_validated_data)
            return version_instance

    def create(self, validated_data):
        version_validated_data = validated_data.pop(self._version_related_name)[0]
        # 创建新模型
        instance = self._model_class.objects.create(**validated_data)
        # 创建新模型版本
        self.create_version(instance, version_validated_data)
        return instance

    def update(self, instance, validated_data):
        """
        更新模型定义为：
          - 使用现有模型不可变字段（TODO：验证模型不变，具体异常方式待定义）
          - 创建模型版本及可变字段

        :param instance:
        :param validated_data:
        :return:
        """
        # 创建新模型版本
        version_validated_data = validated_data.pop(self._version_related_name)[0]
        self.create_version(instance, version_validated_data)
        return instance
