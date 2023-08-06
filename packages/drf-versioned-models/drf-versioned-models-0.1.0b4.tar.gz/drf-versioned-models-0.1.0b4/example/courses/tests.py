from rest_framework import status
from rest_framework.test import APITestCase


class CourseAPITestCase(APITestCase):
    """
    TODO: 固定手动集成测试。
    """
    fixtures = ['courses.json']

    def test_list_courses(self):
        pass

    def test_curd_course(self):
        pass
