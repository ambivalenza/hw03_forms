# deals/tests/tests_models.py
from django.test import TestCase
from ..models import Post, Group


class TaskModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

