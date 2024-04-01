import sqlalchemy
from sqlalchemy import create_engine, text

db_connection_string = "sqlite:///momcons.db"

engine = create_engine(db_connection_string, echo=True)


def load_domdoms_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM momcons"))
        rows = result.fetchall()  # fetch all rows
        domdoms_lst = []
        # Fetch the column names
        keys = result.keys()

        for row in rows:
            # Convert tuple to dictionary
            row_dict = dict(zip(keys, row))
            domdoms_lst.append(row_dict)

        return domdoms_lst


def load_domdom_from_db(dom_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM momcons where id = :val"), {"val": dom_id}
        )
        rows = result.fetchall()  # Fetch all rows, should return one row

        if rows:
            keys = result.keys()  # Fetch the column names
            row_dict = dict(zip(keys, rows[0]))  # Convert tuple to dictionary
            return row_dict
        else:
            return None


def add_to_db(data):
    if not data.get("honeypot"):
        with engine.connect() as conn:
            query = text("INSERT INTO momcons (title, wisdom) VALUES (:title, :wisdom)")
            conn.execute(query, {"title": data["title"], "wisdom": data["wisdom"]})
        return True
    else:
        return False
