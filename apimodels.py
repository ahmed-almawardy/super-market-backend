from datetime import date
from typing import Annotated, Any

from dateutil.parser import parse
from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    HttpUrl,
    field_serializer,
)
from pydantic_core.core_schema import ValidationInfo


class Product(BaseModel):
    id: int
    name: str
    quantity: int = Field(ge=0)
    unit: str = "وحدات"
    expiry_date: date
    image_url: HttpUrl | None = None
    emoji: str | None = None
    is_hidden: bool | None = False


def validate_emoji(value: Any, info: ValidationInfo) -> str | None:
    if isinstance(value, str):
        return value


def validate_date(value: str, info: ValidationInfo):
    return parse(value).date()


class ProductCreate(BaseModel):
    name: str
    quantity: int = Field(ge=0)
    unit: str = "وحدات"
    expiry_date: Annotated[date | str, BeforeValidator(validate_date)]
    image_url: HttpUrl | None = None
    emoji: Annotated[str | None, BeforeValidator(validate_emoji)]
    is_hidden: bool = False

    @field_serializer("image_url")
    def serializer_to_db(self, value: HttpUrl) -> str:
        return value.encoded_string()
