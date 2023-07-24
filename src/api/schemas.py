from pydantic import BaseModel

from datetime import datetime


class PhishingSiteCreate(BaseModel):
    PhishTank_id: int
    url: str
    status: str
    is_online: str
    submitted_at: str
    description: str
    submitted_by: str
    date_created: datetime

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class PhishingSite(PhishingSiteCreate):
    PhishTank_id: int
    url: str
    status: str
    is_online: str
    submitted_at: str
    description: str
    submitted_by: str
    date_created: datetime

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True


class PhishingSiteUpdate(BaseModel):
    status: str
    is_online: str
    description: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
