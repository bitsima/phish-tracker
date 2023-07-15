from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import read_credentials


Base = declarative_base()


class PhishingSite(Base):
    __tablename__ = "phishing_sites"

    PhishTank_id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    status = Column(Enum("Suspected", "Valid"), nullable=False)
    added_at = Column(String, nullable=False)
    description = Column(String)
    submitted_by = Column(String, nullable=False)


def add_to_db(
    PhishTank_id: int,
    url: str,
    status: Enum,
    added_at: str,
    description: str,
    submitted_by: str,
) -> None:
    session = Session()

    new_site = PhishingSite(
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


credentials = read_credentials()

engine = create_engine(
    f"postgresql+psycopg2://{credentials[0]}:{credentials[1]}@localhost:5432/database"
)

Session = sessionmaker(bind=engine)
