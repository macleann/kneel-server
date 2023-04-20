import sqlite3
import json
from models import Metal

def get_all_metals():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.metal,
            m.price
        FROM Metals m
        """)

        metals = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            metal = Metal(row['id'], row['metal'], row['price'])
            metals.append(metal.__dict__)

    return metals

def get_single_metal(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.metal,
            m.price
        FROM Metals m
        WHERE m.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        metal = Metal(data['id'], data['metal'], data['price'])
        return metal.__dict__

def create_metal(metal):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Metals
            ( metal, price )
        VALUES
            ( ? , ? )
        """, (metal['metal'], metal['price']))

        id = db_cursor.lastrowid
        metal['id'] = id

    return metal

def update_metal(id, new_metal):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Metals
            SET
                metal = ?,
                price = ?
        WHERE id = ?
        """, (new_metal['metal'], new_metal['price'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True

def delete_metal(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Metals
        WHERE id = ?
        """, ( id, ))
