import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import dotenv
from dotenv.main import DotEnv

# Define database url
SQLALCHEMY_DATABASE_URL = DotEnv(dotenv.find_dotenv()).dict()["DATABASE_URL"]

# Define db model base
metadata = sqlalchemy.MetaData()
Base = declarative_base(metadata=metadata)

# Create the database engine and session
db_engine = create_engine(SQLALCHEMY_DATABASE_URL)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
)
