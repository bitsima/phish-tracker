from pydantic import BaseModel
from sqlalchemy import Enum

import datetime


class PhishingSiteCreate(BaseModel):
    PhishTank_id: int
    url: str
    status: Enum
    is_online: Enum
    submitted_at: str
    submitted_by: str


class PhishingSite(PhishingSiteCreate):
    PhishTank_id: int
    url: str
    status: Enum
    is_online: Enum
    submitted_at: str
    description: str
    submitted_by: str
    date_created = datetime.datetime
