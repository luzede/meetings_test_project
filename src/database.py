from sqlalchemy.orm.session import sessionmaker, Session
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from dotenv import dotenv_values, find_dotenv
from src.models import Base, User, Meeting
import datetime

config = dotenv_values(find_dotenv())

connection_string = URL.create(
    drivername="postgresql+psycopg",
    username=config.get("PGUSER"),
    password=config.get("PGPASSWORD"),
    host=config.get("PGHOST"),
    database=config.get("PGDATABASE"),
)
print(connection_string)

engine = create_engine(
    connection_string, echo=True, connect_args={"sslmode": "require"}
)

MakeSession = sessionmaker(bind=engine, expire_on_commit=False)


def db_init():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return MakeSession()
