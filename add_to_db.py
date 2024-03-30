from create_db import Session, MomCon

# Create a session instance
session = Session()
print("Session instance created.")

# Create a new MomCon instance
new_momcon = MomCon(
    title="Babylon",
    wisdom="Simon Cowell can't write a song. In the world of Simon Cowell, we'd have no music. Somebody has to do the building.",
)
print(
    f"New MomCon instance created: Title - {new_momcon.title}, Wisdom - {new_momcon.wisdom}"
)

# Add the new instance to the session and commit it to the database
session.add(new_momcon)
print("New MomCon instance added to the session.")

session.commit()
print("Session committed to the database.")

# Fetch and print all MomCon entries
all_momcons = session.query(MomCon).all()
print("All MomCon entries fetched from the database:")
for momcon in all_momcons:
    print(f"ID: {momcon.id}, Title: {momcon.title}, Wisdom: {momcon.wisdom}")
