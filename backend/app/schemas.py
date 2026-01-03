from pydantic import BaseModel, HttpUrl
from datetime import datetime

class ShortenRequest(BaseModel):
    long_url: HttpUrl
    custom_alias: str | None = None
    expiration_date: datetime | None = None

class ShortenResponse(BaseModel):
    short_url: str
    short_code: str
