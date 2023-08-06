from datetime import datetime, timezone
from unittest import TestCase

from pydantic.types import UUID

from python_sdk.models.application import Application

from ._helpers import get_application_data

NOW = datetime(2022, 9, 19, 16, 0, 0, tzinfo=timezone.utc)


class ApplicationTestCase(TestCase):
    def test_creation(self):
        application = Application(**get_application_data())
        self.assertEqual(application.id, UUID('3c819c1d-6587-448d-8ba4-3b6f23e87ed4'))
