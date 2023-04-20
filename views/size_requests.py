import sqlite3
import json
from models import Size

def get_all_sizes():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.carets,
            s.price
        FROM Sizes s
        """)

        sizes = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            size = Size(row['id'], row['carets'], row['price'])
            sizes.append(size.__dict__)

    return sizes

def get_single_size(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.carets,
            s.price
        FROM Sizes s
        WHERE s.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        size = Size(data['id'], data['carets'], data['price'])
        return size.__dict__

def create_size(size):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Sizes
            ( carets, price )
        VALUES
            ( ? , ? )
        """, (size['carets'], size['price']))

        id = db_cursor.lastrowid
        size['id'] = id

    return size

def update_size(id, new_size):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE sizes
            SET
                carets = ?,
                price = ?
        WHERE id = ?
        """, (new_size['carets'], new_size['price'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True

def delete_size(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Sizes
        WHERE id = ?
        """, ( id, ))
