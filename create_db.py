import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for SQLAlchemy models
Base = declarative_base()


# Define the MomCon model
class MomCon(Base):
    __tablename__ = "momcons"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    wisdom = Column(String)


# Establish a connection to the database
db_connection_string = "sqlite:///placeholder.db"
engine = create_engine(db_connection_string, echo=True)
print("Engine created for database:", db_connection_string)

# Create a Session class bound to the engine
Session = sessionmaker(bind=engine)
print("Session class created.")

if __name__ == "__main__":
    # This block will only run when create_db.py is executed directly,
    # not when it's imported by another module
    print("Creating database and tables...")
    Base.metadata.create_all(engine)
    print("Database and tables created.")
