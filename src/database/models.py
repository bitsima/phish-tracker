from sqlalchemy import Column, Integer, String

import datetime

from . import database


class PhishingSite(database.Base):
    __tablename__ = "phishing_sites"

    PhishTank_id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    status = Column(String, nullable=False)
    is_online = Column(String)
    submitted_at = Column(String, nullable=False)
    description = Column(String)
    submitted_by = Column(String, nullable=False)
    date_created = datetime.datetime.now()
