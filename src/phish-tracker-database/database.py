from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import read_credentials


credentials = read_credentials()
DATABASE_URL = (
    f"postgresql+psycopg2://{credentials[0]}:{credentials[1]}@localhost:5432/database"
)
engine = create_engine(DATABASE_URL)

Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
