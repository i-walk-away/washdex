from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PriceComponent(BaseModel):
    IncludeServiceAmount: int
    AdditionalServiceAmounts: dict[str, dict]


class PriceElement(BaseModel):
    Id: str
    StartTime: dict
    EndTime: dict
    ClientGroup: list[str]
    PriceComponent: dict[str, PriceComponent]


class Tariff(BaseModel):
    _id: str
    Name: str
    Description: str
    PriceElements: list[PriceElement]
    IncludeService: list[str]
    AdditionService: list[str]
    DurationMinutes: dict[str, int]


class CarWashData(BaseModel):
    _id: str
    carwash_id: str
    network_id: str
    DateCreate: datetime
    StartDateTime: datetime
    EndDateTime: Optional[datetime]
    Tariffs: list[Tariff]
