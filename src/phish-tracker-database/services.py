from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import sessionmaker

from . import _database
from . import models


def create_schema():
    database = _database.Base.metadata.create_all(bind=_database.engine)
    return database


def add_to_db(
    PhishTank_id: Integer,
    url: String,
    status: Enum,
    added_at: String,
    description: String,
    submitted_by: String,
) -> None:
    session = sessionmaker.Session()

    new_site = models.PhishingSite(
        PhishTank_id=PhishTank_id,
        url=url,
        status=status,
        added_at=added_at,
        description=description,
        submitted_by=submitted_by,
    )

    session.add(new_site)
    session.commit()
    session.close()


def remove_from_db(PhishTank_id: int) -> None:
    pass
