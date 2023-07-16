from pydantic import BaseModel
from sqlalchemy import Enum

from datetime import datetime


class StatusEnum(Enum):
    SUSPECTED = "Suspected"
    VALID = "Valid"


class IsOnlineEnum(Enum):
    TRUE = "True"
    FALSE = "False"


class PhishingSiteCreate(BaseModel):
    PhishTank_id: int
    url: str
    status: Enum
    is_online: Enum
    submitted_at: str
    submitted_by: str

    class Config:
        arbitrary_types_allowed = True


class PhishingSiteUpdate(BaseModel):
    status: Enum
    is_online: Enum
    description: str

    class Config:
        arbitrary_types_allowed = True


class PhishingSite(PhishingSiteCreate):
    PhishTank_id: int
    url: str
    status: Enum
    is_online: Enum
    submitted_at: str
    description: str
    submitted_by: str
    date_created: datetime

    class Config:
        arbitrary_types_allowed = True
