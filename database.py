import sqlalchemy
from sqlalchemy import create_engine, text
import random
import os
import pymysql


db_connection_string = os.environ["DB_CONNECTION_STRING"]


engine = create_engine(db_connection_string, echo=True)


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
    with engine.connect() as conn:
        result = conn.execute(
            text("select * from domdoms3 where id = :val"), {"val": dom_id}
        )
        rows = result.fetchall()  # Fetch all rows, should return one row

        if rows:
            keys = result.keys()  # Fetch the column names
            row_dict = dict(zip(keys, rows[0]))  # Convert tuple to dictionary
            return row_dict
        else:
            return None


def add_to_db(data):
    if data.get("honeypot"):
        print("Honeypot check failed")
        return False

    with engine.connect() as conn:
        query = text("INSERT INTO domdoms3 (title, wisdom) VALUES (:title, :wisdom)")
        conn.execute(query, title=data["title"], wisdom=data["wisdom"])
    return True
