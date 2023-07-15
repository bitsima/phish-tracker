from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import sessionmaker

from . import _database
from . import models


def add_tables():
    database = _database.Base.metadata.create_all(bind=_database.engine)
    return database


def add_to_db(
    PhishTank_id: Integer,
    url: String,
    status: Enum,
    is_online: Enum,
    added_at: String,
    description: String,
    submitted_by: String,
) -> None:
    session = sessionmaker.Session()

    new_site = models.PhishingSite(
        PhishTank_id=PhishTank_id,
        url=url,
        status=status,
        is_online=is_online,
        added_at=added_at,
        description=description,
        submitted_by=submitted_by,
    )

    session.add(new_site)
    session.commit()
    session.close()


def remove_from_db(PhishTank_id: int) -> None:
    pass
