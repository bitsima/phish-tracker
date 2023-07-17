from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytest

from ..src import database
from ..src import utils


@pytest.fixture(scope="function")
def database():
    # setup
    credentials = utils.read_credentials()

    engine = create_engine(
        f"postgresql+psycopg2://{credentials[0]}:{credentials[1]}@localhost:5432/database"
    )

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # teardown
    session.close()
    engine.dispose()
