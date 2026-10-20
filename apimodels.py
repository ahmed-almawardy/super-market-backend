from datetime import date
from typing import Optional, Annotated, Any

from pydantic import BaseModel, Field, HttpUrl, field_validator, field_serializer, BeforeValidator
from pydantic_core.core_schema import ValidationInfo
from dateutil.parser import parse


class Product(BaseModel):
    id: int
    name: str
    quantity: int = Field(ge=0)
    unit: str = "وحدات"
    expiry_date: date
    image_url: Optional[HttpUrl] = None
    emoji: Optional[str] = None




def validate_emoji(value: Any, info: ValidationInfo) -> Optional[str]:
    if isinstance(value, str):
        return value


def validate_date(value: str, info: ValidationInfo):
    return parse(value).date()



class ProductCreate(BaseModel):
    name: str
    quantity: int = Field(ge=0)
    unit: str = "وحدات"
    expiry_date: Annotated[date | str, BeforeValidator(validate_date)]
    image_url: Optional[HttpUrl] = None
    emoji: Annotated[Optional[str], BeforeValidator(validate_emoji)]
