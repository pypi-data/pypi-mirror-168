import unittest

from django.test import TestCase

from drf_versioned_models.models import VersionedModel, ModelVersion
from .models import ExampleModel, ExampleModelVersion


class VersionedModelTestCase(TestCase):
    model_class = ExampleModel
    fixtures = ['examples.json']

    def test_init(self):
        model_instance = self.model_class()
        self.assertIsInstance(model_instance, VersionedModel)
        self.assertTrue(model_instance.is_active)

    def test_delete(self):
        model_instance = self.model_class.objects.get()
        model_instance.delete()
        self.assertFalse(model_instance.is_active)


class ModelVersionTestCase(TestCase):
    model_class = ExampleModelVersion
    fixtures = ['examples.json']

    def test_init(self):
        model_instance = self.model_class()
        self.assertIsInstance(model_instance, ModelVersion)
        self.assertTrue(model_instance.is_active)

    def test_delete(self):
        model_instance = self.model_class.objects.get(version='0.1.0')
        model_instance.delete()
        self.assertFalse(model_instance.is_active)

