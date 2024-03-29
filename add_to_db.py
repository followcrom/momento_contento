from create_db import Session, MomCon

# Create a session instance
session = Session()
print("Session instance created.")

# Create a new MomCon instance
new_momcon = MomCon(
    title="Only A Brit Can Drop The Bard",
    wisdom="Perdition catch my soul, But I do love thee! And when I love thee not, Chaos is come again.",
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
