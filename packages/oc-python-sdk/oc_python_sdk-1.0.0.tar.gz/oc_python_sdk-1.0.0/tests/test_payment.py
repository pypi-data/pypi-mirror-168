import json
from datetime import datetime, timezone
from unittest import TestCase

from freezegun import freeze_time
from pydantic.error_wrappers import ValidationError
from pydantic.types import UUID

from python_sdk.models.payment import CurrencyType, HttpMethodType, PayerType, Payment, PaymentStatus, PaymentType

from ._helpers import get_payment_data

NOW = datetime(2022, 9, 19, 16, 0, 0, tzinfo=timezone.utc)


class PaymentTestCase(TestCase):
    def test_creation(self):
        payment = Payment(**get_payment_data())
        self.assertEqual(payment.id, UUID('bb7044e4-066c-4bf7-915e-87ee97270eae'))
        payment.payment.paid_at = 'non-valid-datetime'

    def test_iso_date(self):
        with self.assertRaises(ValidationError):
            Payment(**get_payment_data(created_at='non-valid-datetime'))

    def test_payment_creation(self):
        self.assertTrue(
            Payment(**get_payment_data(status=PaymentStatus.STATUS_CREATION_PENDING)).is_payment_creation_needed(),
        )
        self.assertFalse(
            Payment(**get_payment_data(status=PaymentStatus.STATUS_COMPLETE)).is_payment_creation_needed(),
        )

    def test_update_time(self):
        payment = Payment(**get_payment_data())
        with freeze_time(NOW):
            payment.update_time('updated_at')
            self.assertEqual(payment.updated_at, NOW.isoformat())

    def test_encoders(self):
        payment = Payment(**get_payment_data())

        self.assertEqual(json.loads(payment.json())['id'], 'bb7044e4-066c-4bf7-915e-87ee97270eae')
        self.assertEqual(json.loads(payment.json())['created_at'], '2022-06-08T08:28:42+00:00')
        self.assertEqual(json.loads(payment.status.json()), PaymentStatus.STATUS_CREATION_PENDING.value)
        self.assertEqual(json.loads(payment.type.json()), PaymentType.TYPE_PAGOPA.value)
        self.assertEqual(json.loads(payment.payer.type.json()), PayerType.TYPE_HUMAN.value)
        self.assertEqual(json.loads(payment.payment.currency.json()), CurrencyType.CURRENCY_EUR.value)
        self.assertEqual(json.loads(payment.links.notify[0].method.json()), HttpMethodType.HTTP_METHOD_POST.value)
