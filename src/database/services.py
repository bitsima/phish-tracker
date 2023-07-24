"""Yields sessions and interacts with the database.

Contains the following functions:
add_tables()
get_db()
create_site(site: schemas.PhishingSiteCreate, db: orm.Session) -> schemas.PhishingSite
get_last_saved(db: orm.Session) -> models.PhishingSite
get_all_sites(db: orm.Session) -> list[schemas.PhishingSite]
update_site(site_data: schemas.PhishingSiteUpdate, site: models.PhishingSite, db: orm.Session) -> schemas.PhishingSite
delete_site(site: models.PhishingSite, db: orm.Session) -> None
"""

from sqlalchemy import orm

from . import database as _database
from . import models
from ..api import schemas


def add_tables():
    database = _database.Base.metadata.create_all(bind=_database.engine)
    return database


def get_db() -> orm.Session:
    """Used to get new local session instances for the database.

    Yields:
        orm.Session: a new local session instance
    """
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_site(
    site: schemas.PhishingSiteCreate, db: orm.Session
) -> schemas.PhishingSite:
    """Creates the model object to be stored in the database from the schema, adds and commits it to the database.

    Args:
        site (schemas.PhishingSiteCreate): the new schema object to be stored in the database
        db (orm.Session): a local session instance

    Returns:
        schemas.PhishingSite: the schema object generated from the model object stored in the database
    """
    site = models.PhishingSite(**site.model_dump())
    db.add(site)
    db.commit()
    db.refresh(site)

    return schemas.PhishingSite(**site.__dict__)


async def get_last_saved(db: orm.Session) -> models.PhishingSite:
    """Returns the latest site entry, after sorting by posts' submission timestamps.

    Args:
        db (orm.Session): a local session instance

    Returns:
        models.PhishingSite: the last post fetched from PhishTank stored in the database, as a model instance.
    """
    last_saved = (
        db.query(models.PhishingSite)
        .order_by(models.PhishingSite.submitted_at.desc())
        .first()
    )
    return last_saved


async def get_all_sites(db: orm.Session) -> list[schemas.PhishingSite]:
    """Queries the database for all site entries and returns the result as a list after converting models into schemata.

    Args:
        db (orm.Session): a local session instance

    Returns:
        list[schemas.PhishingSite]: the list of all schema instances of PhishingSite
    """
    sites = db.query(models.PhishingSite).all()
    return list(map(schemas.PhishingSite.from_orm, sites))


async def get_site(PhishTank_id: int, db: orm.session) -> models.PhishingSite:
    """Queries the database for the url with the given id and returns the corresponding model instance.

    Args:
        PhishTank_id (int): id of the site object, also primary key in the database
        db (orm.session): a local session instance

    Returns:
        models.PhishingSite: the corresponding model object
    """
    site = (
        db.query(models.PhishingSite)
        .filter(models.PhishingSite.PhishTank_id == PhishTank_id)
        .first()
    )
    return site


async def update_site(
    site_data: schemas.PhishingSiteUpdate, site: models.PhishingSite, db: orm.Session
) -> dict:
    """Helps update site objects' validity and online status.

    Args:
        site_data (schemas.PhishingSiteUpdate): most recent validity data, in the form of PhishingSiteUpdate schema.
        site (models.PhishingSite): the original model object from the database
        db (orm.Session): a local session instance

    Returns:
        dict: the dictionary containing all update messages for a single object
    """
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
    """Deletes the site object from the database and commits changes.

    Args:
        site (models.PhishingSite): model object to be deleted
        db (orm.Session): a local session instance
    """
    db.delete(site)
    db.commit()
