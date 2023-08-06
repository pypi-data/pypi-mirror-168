import datetime
import functools
import json
from enum import Enum
from json import JSONEncoder
from typing import List, Union
from uuid import UUID

from dateutil import parser
from pydantic import BaseModel, validator

from ..utils.logger import payment_logger as logger


def check_iso_format(v: str):
    try:
        return parser.parse(v)
    except Exception:
        raise ValueError('date must be ISO8601 format')


def check_isoformat_none_case(v: Union[str, None]):
    if v is not None:
        try:
            return parser.parse(v)
        except Exception:
            raise ValueError('date must be ISO8601 format')


class HttpMethodType(Enum):
    HTTP_METHOD_GET = 'GET'
    HTTP_METHOD_POST = 'POST'

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class CurrencyType(Enum):
    CURRENCY_EUR = 'EUR'

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class PaymentStatus(Enum):
    STATUS_CREATION_PENDING = 'CREATION_PENDING'
    STATUS_CREATION_FAILED = 'CREATION_FAILED'
    STATUS_PAYMENT_PENDING = 'PAYMENT_PENDING'
    STATUS_PAYMENT_STARTED = 'PAYMENT_STARTED'
    STATUS_PAYMENT_CONFIRMED = 'PAYMENT_CONFIRMED'
    STATUS_PAYMENT_FAILED = 'PAYMENT_FAILED'
    STATUS_NOTIFICATION_PENDING = 'NOTIFICATION_PENDING'
    STATUS_COMPLETE = 'COMPLETE'
    STATUS_EXPIRED = 'EXPIRED'

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class PaymentType(Enum):
    TYPE_PAGOPA = 'PAGOPA'

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class PayerType(Enum):
    TYPE_HUMAN = 'human'
    TYPE_LEGAL = 'legal'

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class PaymentDataSplit(BaseModel):
    code: str
    amount: float
    meta: dict

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class PaymentData(BaseModel):
    transaction_id: Union[UUID, None]
    paid_at: Union[str, None]
    expire_at: str
    amount: float
    currency: CurrencyType
    notice_code: Union[str, None]
    iud: str
    iuv: Union[str, None]
    split: Union[List[PaymentDataSplit], List[None]]

    paid_at_must_be_iso8601 = validator('paid_at', allow_reuse=True)(check_isoformat_none_case)
    expire_at_must_be_iso8601 = validator('expire_at', allow_reuse=True)(check_iso_format)

    def split_append(self, split):
        for item in split:
            self.split.append(PaymentDataSplit(**item))

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class OnlinePaymentBegin(BaseModel):
    url: Union[str, None]
    last_opened_at: Union[str, None]
    method: Union[HttpMethodType, None]

    last_opened_at_must_be_iso8601 = validator('last_opened_at', allow_reuse=True)(check_isoformat_none_case)

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class OnlinePaymentLanding(OnlinePaymentBegin):
    pass


class OfflinePayment(OnlinePaymentBegin):
    pass


class Receipt(OnlinePaymentBegin):
    pass


class Notify(BaseModel):
    url: str
    method: HttpMethodType
    sent_at: Union[str, None]

    sent_at_must_be_iso8601 = validator('sent_at', allow_reuse=True)(check_isoformat_none_case)

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class Update(BaseModel):
    url: Union[str, None]
    last_check_at: Union[str, None]
    next_check_at: Union[str, None]
    method: Union[HttpMethodType, None]

    last_check_at_must_be_iso8601 = validator('last_check_at', allow_reuse=True)(check_isoformat_none_case)
    next_check_at_must_be_iso8601 = validator('next_check_at', allow_reuse=True)(check_isoformat_none_case)

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class Links(BaseModel):
    online_payment_begin: OnlinePaymentBegin
    online_payment_landing: OnlinePaymentLanding
    offline_payment: OfflinePayment
    receipt: Receipt
    notify: List[Notify]
    update: Update

    def append_notify(self, notify):
        for item in notify:
            self.notify.append(Notify(**item))

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class Payer(BaseModel):
    type: PayerType
    tax_identification_number: str
    name: str
    family_name: Union[str, None]
    street_name: Union[str, None]
    building_number: Union[str, None]
    postal_code: Union[str, None]
    town_name: Union[str, None]
    country_subdivision: Union[str, None]
    country: Union[str, None]
    email: Union[str, None]

    @validator('country')
    def country_must_be_it(cls, v):
        if 'IT' not in v:
            raise ValueError('country must be IT')
        return v

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class Payment(BaseModel):
    id: UUID
    user_id: UUID
    type: PaymentType
    tenant_id: UUID
    service_id: UUID
    created_at: str
    updated_at: str
    status: PaymentStatus
    reason: str
    remote_id: UUID
    payment: PaymentData
    links: Links
    payer: Payer
    event_id: UUID
    event_version: str
    event_created_at: str
    app_id: str

    @validator('reason')
    def reason_must_be_lteq_140_chars(cls, v):
        if len(v) > 140:
            raise ValueError('reason must be less than or equal to 140 characters')
        return v

    created_at_must_be_iso8601 = validator('created_at', allow_reuse=True)(check_iso_format)
    updated_at_must_be_iso8601 = validator('updated_at', allow_reuse=True)(check_iso_format)

    @validator('event_version')
    def event_version_must_be_two(cls, v):
        if '1' not in v:
            raise ValueError('event must have 1.0 as version')
        return v.title()

    event_created_at_must_be_iso8601 = validator('event_created_at', allow_reuse=True)(check_iso_format)

    def update_time(self, field):
        self._rsetattr(
            field,
            datetime.datetime.now().replace(microsecond=0).astimezone().isoformat(),
        )
        return self

    def update_check_time(self):
        if not self.links.update.next_check_at:
            return self

        last_check = parser.parse(self.links.update.last_check_at)
        now = datetime.datetime.now()
        next_check = None

        week_checkpoint = self.created_at + datetime.timedelta(days=7)
        month_checkpoint = self.created_at + datetime.timedelta(days=30)
        year_checkpoint = self.created_at + datetime.timedelta(days=365)

        if last_check <= week_checkpoint:
            next_check = now + datetime.timedelta(hours=1)
        elif last_check <= month_checkpoint:
            next_check = now + datetime.timedelta(hours=6)
        elif last_check <= year_checkpoint:
            days_ahead = 6 - now.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            next_check = now + datetime.timedelta(days=days_ahead)

        self.links.update.next_check_at = next_check.replace(microsecond=0).astimezone().isoformat()
        return self

    def _rsetattr(self, attr, val):
        pre, _, post = attr.rpartition('.')
        return setattr(self._rgetattr(pre) if pre else self, post, val)

    def _rgetattr(self, attr, *args):
        def _getattr(obj, attr):
            return getattr(obj, attr, *args)

        return functools.reduce(_getattr, [self] + attr.split('.'))

    def is_payment_creation_needed(self):
        if self.status != PaymentStatus.STATUS_CREATION_PENDING:
            logger.info(f'Event {self.id} from application {self.remote_id}: Payment creation not required')
            return False
        return True

    def json(self):
        return json.dumps(self, cls=PaymentEncoder)


class PaymentEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        elif isinstance(o, UUID):
            return str(o)
        elif isinstance(o, (PaymentType, PayerType, PaymentStatus, HttpMethodType, CurrencyType)):
            return o.value
        return o.__dict__
