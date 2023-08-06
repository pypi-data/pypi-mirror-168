"""
测试数据
"""
import json
from collections import OrderedDict
from datetime import datetime

from tests.models import ExampleModel


class TestDataMixin:
    fixtures = ['examples.json']

    @classmethod
    def setUpTestData(cls):
        cls.instance = ExampleModel.objects.get(name='data-analytics-with-python')
        cls.serialized_data = {
            'id': "61741d93-8db4-4845-83c9-7e625e445983",
            'name': 'data-analytics-with-python',
            'version': '0.1.0',
            "title": "Python数据分析",
            "created_at": "2022-05-23T00:00:00",
            "updated_at": '2022-05-23T00:00:00'
        }
        cls.new_data = {
            'name': 'test-name',
            "created_at": "2022-05-23T00:00:00",
            'title': '测试标题',
            'version': '0.1.0',
            'updated_at': '2022-05-24T00:00:00',
        }
        cls.deserialized_data = {
            'name': 'test-name',
            "created_at": datetime.fromisoformat("2022-05-23T00:00:00"),
            'versions': [
                {
                    'version': '0.1.0',
                    'title': '测试标题',
                    'created_at': datetime.fromisoformat('2022-05-24T00:00:00')
                }
            ]
        }
        cls.new_version_data = {
            'name': 'data-analytics-with-python',
            "created_at": "2022-05-23T00:00:00",
            'title': '测试标题2',
            'version': '0.2.0',
            'updated_at': "2022-05-25T00:00:00",
        }
        cls.new_version_partial_data = {
            'name': 'data-analytics-with-python',
            'version': '0.2.1',
            'updated_at': "2022-05-26T00:00:00",
        }

    def assertOrderedDictEqual(self, obj1, obj2):
        def convert_ordered_dict_to_dict(ordered_dict_obj):
            def json_serial(value):
                if isinstance(value, datetime):
                    return value.isoformat()
                return str(value)
            return json.loads(json.dumps(ordered_dict_obj, default=json_serial))
        self.assertDictEqual(convert_ordered_dict_to_dict(obj1), convert_ordered_dict_to_dict(obj2))
