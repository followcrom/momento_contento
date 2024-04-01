from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Assuming the engine and Base are already defined and the tables created in the first file.
# We just need to connect to the existing database.
engine = create_engine('sqlite:///app/momcons.db')
Base = declarative_base()

# Define your data model again. It's needed to map the Python classes to the database tables.
class MomCon(Base):
    __tablename__ = "momcons"
    id = Column(Integer, primary_key=True)
    title = Column(String(75), unique=True, nullable=False)
    wisdom = Column(String(500), unique=True, nullable=False)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

# Create a session class bound to this engine
Session = sessionmaker(bind=engine)

# Class to perform CRUD operations
class MomConCRUD:
    def __init__(self):
        # Each instance of this class will start a new session
        self.session = Session()

    def create(self, title, wisdom):
        # Create a new MomCon record
        new_momcon = MomCon(title=title, wisdom=wisdom)
        self.session.add(new_momcon)
        self.session.commit()
        print(f"MomCon '{title}' created.")

    def read(self):
        # Read all MomCon records
        momcons = self.session.query(MomCon).all()
        return momcons

    def delete(self, id):
        # Delete a MomCon record by ID
        momcon = self.session.query(MomCon).filter(MomCon.id == id).first()
        if momcon:
            self.session.delete(momcon)
            self.session.commit()
            print(f"MomCon with ID {id} deleted.")

    def close_session(self):
        # Close the session when done
        self.session.close()
        print("Session closed.")


print("---------------------------------------------------------------")

# Create an instance of the CRUD class
crud = MomConCRUD()

# Create a new MomCon
crud.create("Internetwork(ing)", 'The Internet was built partly by the government and partly by private firms, but mostly it was the creation of a loosely knit cohort of academics and hackers who worked as peers and freely shared their creative ideas. The result of such peer sharing was a network that facilitated peer sharing. This was not mere happenstance. The Internet was built with the belief that power should be distributed rather than centralized and that any authoritarian diktats should be circumvented. As Dave Clark, one of the early participants in the Internet Engineering Task Force, put it, “We reject kings, presidents, and voting. We believe in rough consensus and running code.”')

# Read all MomCons
momcons = crud.read()
for momcon in momcons:
    print(f"ID: {momcon.id}, Title: {momcon.title}, Wisdom: {momcon.wisdom}")

# Close the session
crud.close_session()
