import sqlite3
import json
from models import Style

def get_all_styles(query_params):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        sort_by = ""

        if len(query_params) != 0:
            param = query_params[0]
            [qs_key, qs_value] = param.split("=")

            if qs_key == "_sortBy":
                if qs_value == 'price':
                    sort_by = " ORDER BY price"

        db_cursor.execute(f"""
        SELECT
            s.id,
            s.style_type,
            s.price
        FROM Styles s
        {sort_by}
        """)

        styles = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            style = Style(row['id'], row['style_type'], row['price'])
            styles.append(style.__dict__)

    return styles

def get_single_style(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            s.id,
            s.style_type,
            s.price
        FROM Styles s
        WHERE s.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        style = Style(data['id'], data['style_type'], data['price'])
        return style.__dict__

def create_style(style):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Styles
            ( style_type, price )
        VALUES
            ( ? , ? )
        """, (style['style_type'], style['price']))

        id = db_cursor.lastrowid
        style['id'] = id

    return style

def update_style(id, new_style):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Styles
            SET
                style_type = ?,
                price = ?
        WHERE id = ?
        """, (new_style['style_type'], new_style['price'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True

def delete_style(id):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Styles
        WHERE id = ?
        """, ( id, ))
