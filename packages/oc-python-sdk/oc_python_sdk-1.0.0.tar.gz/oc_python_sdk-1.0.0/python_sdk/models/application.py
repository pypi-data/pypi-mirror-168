from enum import Enum
from typing import List, Union
from uuid import UUID

from dateutil import parser
from pydantic import BaseModel, Field, validator


def check_iso_format(v: str):
    try:
        return parser.parse(v)
    except Exception:
        raise ValueError('date must be ISO8601 format')


class AHttpMethodType(Enum):
    HTTP_METHOD_GET = 'GET'
    HTTP_METHOD_POST = 'POST'


class GenericRequest(BaseModel):
    url: str
    method: AHttpMethodType


class Landing(GenericRequest):
    pass


class ANotify(GenericRequest):
    pass


class APaymentDataSplit(BaseModel):
    code: str
    amount: float
    meta: dict


class APaymentData(BaseModel):
    reason: str
    amount: float
    expire_at: str
    split: Union[List[APaymentDataSplit], List[None]]
    notify: ANotify
    landing: Landing

    expire_at_must_be_iso8601 = validator('expire_at', allow_reuse=True)(check_iso_format)


class Applicant(BaseModel):
    email_address: str = Field(None, alias='applicant.data.email_address')
    natoAIl: str = Field(None, alias='applicant.data.Born.data.natoAIl')
    place_of_birth: str = Field(None, alias='applicant.data.Born.data.place_of_birth')
    gender: str = Field(None, alias='applicant.data.gender.data.gender')
    address: str = Field(None, alias='applicant.data.address.data.address')
    house_number: str = Field(None, alias='applicant.data.address.data.house_number')
    municipality: str = Field(None, alias='applicant.data.address.data.municipality')
    county: str = Field(None, alias='applicant.data.address.data.county')
    postal_code: str = Field(None, alias='applicant.data.address.data.postal_code')
    name: str = Field(alias='applicant.data.completename.data.name')
    surname: str = Field(alias='applicant.data.completename.data.surname')
    fiscal_code: str = Field(alias='applicant.data.fiscal_code.data.fiscal_code')

    natoAIl_must_be_iso8601 = validator('natoAIl', allow_reuse=True)(check_iso_format)


# TODO: gestire anagrafiche con meno dati
class Application(BaseModel):
    id: UUID
    tenant_id: UUID
    service_id: UUID
    user: UUID
    status_name: str
    created_at: str
    payment_data: APaymentData
    applicant: Applicant = Field(alias='data')
    event_version: str
    event_id: UUID

    @validator('status_name')
    def status_name_must_be_status_payment_pending(cls, v):
        if 'status_payment_pending' not in v:
            raise ValueError('status_name must be status_payment_pending')
        return v

    @validator('event_version')
    def event_version_must_be_two(cls, v):
        if '2' not in v:
            raise ValueError('event_version must be 2')
        return v.title()

    created_at_must_be_iso8601 = validator('created_at', allow_reuse=True)(check_iso_format)
