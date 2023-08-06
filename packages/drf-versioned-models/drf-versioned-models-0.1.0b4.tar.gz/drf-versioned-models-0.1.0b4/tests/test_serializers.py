import json

from django.test import TestCase

from tests.data import TestDataMixin
from tests.models import ExampleModel, ExampleModelVersion, ExampleModelVersionRelatedField
from tests.serializers import ExampleModelSerializer, ExampleModelWithTagSerializer


class VersionedModelSerializerTestCase(TestDataMixin, TestCase):
    serializer_class = ExampleModelSerializer

    def test_to_representation(self):
        data = self.serializer_class().to_representation(self.instance)
        self.assertDictEqual(self.serialized_data, json.loads(json.dumps(data)))

    def test_serialization(self):
        serializer = self.serializer_class(self.instance)
        self.assertDictEqual(self.serialized_data, json.loads(json.dumps(serializer.data)))

    def test_validate(self):
        serializer = self.serializer_class(self.instance, data=self.new_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_to_interval_value(self):
        data = self.serializer_class().to_internal_value(self.new_data)
        self.assertOrderedDictEqual(data, self.deserialized_data)

    def test_create(self):
        serializer = self.serializer_class(data=self.new_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()
        self.assertTrue(ExampleModel.objects.get(name=self.new_data['name']))
        self.assertTrue(ExampleModelVersion.objects.filter(version=self.new_data['version']).exists())

    def test_update(self):
        serializer = self.serializer_class(self.instance, data=self.new_version_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()
        self.assertTrue(ExampleModelVersion.objects.filter(version=self.new_version_data['version']).exists())

    def test_partial_update(self):
        serializer = self.serializer_class(self.instance, data=self.new_version_partial_data, partial=True)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()
        version_instance = ExampleModelVersion.objects.get(version=self.new_version_partial_data['version'])
        self.assertEqual(version_instance.title, 'Python数据分析')


class CustomVersionSerializerTestCase(TestDataMixin, TestCase):
    serializer_class = ExampleModelWithTagSerializer

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.serialized_data.update({'tags': ['python']})
        cls.new_data.update({'tags': ['python']})
        cls.new_version_data.update({'tags': ['python']})
        cls.deserialized_data['versions'][0].update({'tags': ['python']})

    def test_to_representation(self):
        data = self.serializer_class().to_representation(self.instance)
        self.assertDictEqual(self.serialized_data, json.loads(json.dumps(data)))

    def test_serialization(self):
        serializer = self.serializer_class(self.instance)
        self.assertDictEqual(self.serialized_data, json.loads(json.dumps(serializer.data)))

    def test_to_interval_value(self):
        data = self.serializer_class().to_internal_value(self.new_data)
        self.assertOrderedDictEqual(data, self.deserialized_data)

    def test_create_version(self):
        """
        TODO: 待补充测试
        :return: 
        """
        pass

    def test_create(self):
        serializer = self.serializer_class(data=self.new_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()
        model = ExampleModel.objects.get(name=self.new_data['name'])
        self.assertTrue(model)
        model_version = ExampleModelVersion.objects.get(model=model, version=self.new_data['version'])
        self.assertTrue(model_version)
        self.assertTrue(ExampleModelVersionRelatedField.objects.filter(model_version=model_version).exists())

    def test_update(self):
        serializer = self.serializer_class(self.instance, data=self.new_version_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()
        model = ExampleModel.objects.get(name=self.new_version_data['name'])
        self.assertTrue(model)
        model_version = ExampleModelVersion.objects.get(model=model, version=self.new_version_data['version'])
        self.assertTrue(model_version)
        self.assertTrue(ExampleModelVersionRelatedField.objects.filter(model_version=model_version).exists())

    def test_partial_update(self):
        serializer = self.serializer_class(self.instance, data=self.new_version_partial_data, partial=True)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()
        model = ExampleModel.objects.get(name=self.new_version_partial_data['name'])
        self.assertTrue(model)
        model_version = ExampleModelVersion.objects.get(model=model, version=self.new_version_partial_data['version'])
        self.assertTrue(model_version)
        self.assertTrue(ExampleModelVersionRelatedField.objects.filter(model_version=model_version).exists())
