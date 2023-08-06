from django.test import SimpleTestCase, override_settings
from django.apps import apps


@override_settings(INSTALLED_APPS=['drf_versioned_models.apps.DrfVersionedModelsConfig'])
class AppConfigTestCase(SimpleTestCase):
    def test_install_app(self):
        self.assertTrue(apps.is_installed('drf_versioned_models'))
        app_config = apps.get_app_config('drf_versioned_models')
        self.assertEqual('drf_versioned_models', app_config.name)
