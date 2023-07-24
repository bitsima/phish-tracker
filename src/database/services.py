from sqlalchemy import orm

from . import database as _database
from . import models
from ..api import schemas


def add_tables():
    database = _database.Base.metadata.create_all(bind=_database.engine)
    return database


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_site(
    site: schemas.PhishingSiteCreate, db: orm.Session
) -> schemas.PhishingSite:
    site = models.PhishingSite(**site.model_dump())
    db.add(site)
    db.commit()
    db.refresh(site)

    return schemas.PhishingSite(**site.__dict__)


async def get_last_saved(db: orm.Session):
    last_saved = (
        db.query(models.PhishingSite)
        .order_by(models.PhishingSite.submitted_at.desc())
        .first()
    )
    return last_saved


async def get_all_sites(db: orm.Session) -> list[schemas.PhishingSite]:
    sites = db.query(models.PhishingSite).all()
    return list(map(schemas.PhishingSite.from_orm, sites))


async def get_site(PhishTank_id: int, db: orm.session) -> models.PhishingSite:
    site = (
        db.query(models.PhishingSite)
        .filter(models.PhishingSite.PhishTank_id == PhishTank_id)
        .first()
    )
    return site


async def update_site(
    site_data: schemas.PhishingSiteUpdate, site: models.PhishingSite, db: orm.Session
) -> schemas.PhishingSite:
    update_message = dict()
    if site.status != site_data.status:
        update_message[
            "message_status"
        ] = f"INFO: Updated site with id {site.PhishTank_id}, changed previous status - {site.status} to {site_data.status}"
    site.status = site_data.status

    if site.is_online != site_data.is_online:
        update_message[
            "message_online"
        ] = f"INFO: Updated site with id {site.PhishTank_id}, changed previous is_online - {site.is_online} to {site_data.is_online}"

    site.is_online = site_data.is_online

    if site.description != site_data.description:
        update_message[
            "message_desc"
        ] = f"INFO: Updated site with id {site.PhishTank_id}, changed previous description - {site.description} to {site_data.description}"
    site.description = site_data.description

    db.commit()
    db.refresh(site)
    return update_message


async def delete_site(site: models.PhishingSite, db: orm.Session) -> None:
    db.delete(site)
    db.commit()
