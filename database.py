import sqlalchemy
from sqlalchemy import create_engine, text
import random
import os
import pymysql


db_connection_string = os.environ["DB_CONNECTION_STRING"]


engine = create_engine(db_connection_string)


def load_domdoms_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from domdoms3"))
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
    numdoms = len(load_domdoms_from_db())
    with engine.connect() as conn:
        result = conn.execute(
            text("select * from domdoms3 where id = :val"), val=dom_id
        )
        rows = result.all()
        return dict(rows[0])


def add_to_db(data):
    if not data.get("honeypot"):
        with engine.connect() as conn:
            query = text(
                "INSERT INTO domdoms3 (title, wisdom) VALUES (:title, :wisdom)"
            )
            conn.execute(query, title=data["title"], wisdom=data["wisdom"])
        return True
    else:
        return False
