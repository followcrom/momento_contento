from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Define the base class for our models.
Base = declarative_base()

# Define the MomCon data model.
class MomCon(Base):
    __tablename__ = "momcons"
    id = Column(Integer, primary_key=True)
    title = Column(String(75), unique=True, nullable=False)
    wisdom = Column(String(500), unique=True, nullable=False)

# Create an engine that connects to a SQLite database file
engine = create_engine('sqlite:///app/momcons.db')

# Bind the engine to the base class, making the connections between our models and the database
Base.metadata.bind = engine

# Create all tables in the database. This is safe to call multiple times (it won't recreate tables).
Base.metadata.create_all(engine)
