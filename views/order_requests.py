import sqlite3
import json
from models import Order, Metal, Style, Size

def get_all_orders():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            o.id,
            o.timestamp,
            o.metal_id,
            m.metal,
            m.price,
            o.style_id,
            st.style_type,
            st.price,
            o.size_id,
            s.carets,
            s.price
        FROM Orders o
        JOIN Metals m ON m.id = o.metal_id
        JOIN Styles st ON st.id = o.style_id
        JOIN Sizes s ON s.id = o.size_id
        """)

        orders = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            order = Order(row['id'], row['timestamp'], row['metal_id'], 
                          row['style_id'], row['size_id'])
            metal = Metal(row['metal_id'], row['metal'], row['price'])
            style = Style(row['style_id'], row['style_type'], row['price'])
            size = Size(row['size_id'], row['carets'], row['price'])
            
            order.metal = metal.__dict__
            order.style = style.__dict__
            order.size = size.__dict__
            orders.append(order.__dict__)

    return orders

def get_single_order(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            o.id,
            o.timestamp,
            o.metal_id,
            o.style_id,
            o.size_id
        FROM Orders o
        WHERE o.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        order = Order(data['id'], data['timestamp'], data['metal_id'],
                      data['style_id'], data['size_id'])
        return order.__dict__

def create_order(order):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Orders
            ( timestamp, metal_id, style_id, size_id )
        VALUES
            ( ? , ? , ? , ? )
        """, (order['timestamp'], order['metal_id'],
                order['style_id'], order['size_id']))

        id = db_cursor.lastrowid
        order['id'] = id

    return order

def update_order(id, new_order):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Orders
            SET
                timestamp = ?,
                metal_id = ?,
                style_id = ?,
                size_id = ?
        WHERE id = ?
        """, (new_order['timestamp'], new_order['metal_id'],
                new_order['style_id'], new_order['size_id'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True

def delete_order(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Orders
        WHERE id = ?
        """, ( id, ))
