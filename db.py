import datetime
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    database=os.getenv("POSTGRES_DATABASE"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor = conn.cursor()


def get_suppliers():
    select_all = "SELECT * FROM suppliers"
    cursor.execute(select_all)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row[0])
    return result


def delete_supplier(name):
    delete_query = "DELETE FROM suppliers WHERE name = %s"
    cursor.execute(delete_query, (name,))
    conn.commit()


def add_supplier(name):
    insert_query = "INSERT INTO suppliers (name) VALUES (%s)"
    cursor.execute(insert_query, (name,))
    conn.commit()


def add_category(name):
    with conn.cursor() as cur:
        cur.execute("SELECT MAX(order_index) FROM categories")
        result = cur.fetchone()
        order_index = result[0] + 1 if result[0] is not None else 1
        cur.execute("INSERT INTO categories (name, order_index) VALUES (%s, %s)", (name, order_index))
    conn.commit()


def delete_category(name):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM categories WHERE name = %s", (name,))
    conn.commit()


def change_category(name, new_name):
    with conn.cursor() as cur:
        cur.execute("UPDATE categories SET name = %s WHERE name = %s", (new_name, name))
    conn.commit()


def change_order(arr):
    with conn.cursor() as cur:
        for data in arr:
            print(data)
            cur.execute("UPDATE categories SET order_index = %s WHERE name = %s", (data["order_index"], data["name"]))
    conn.commit()


def get_all_categories():
    with conn.cursor() as cur:
        cur.execute("SELECT name, order_index FROM categories")
        rows = cur.fetchall()
    return [dict(name=row[0], order_index=row[1]) for row in rows]


def get_all_items():
    with conn.cursor() as cur:
        cur.execute("SELECT * from items")
        rows = cur.fetchall()
    return [dict(name=row[0], date=row[1], price=row[2], supplier_name=row[3], synonyms=row[4]) for row in rows]


def create_new_item(name, synonyms, category):
    with conn.cursor() as cur:
        cur.execute('INSERT INTO items (name, date, synonyms, category) VALUES (%s, NOW(), %s, %s)',
                    (name, synonyms, category))
        conn.commit()


def edit_item(name, synonyms, category):
    with conn.cursor() as cur:
        cur.execute('UPDATE items SET date = NOW(), synonyms = %s, category = %s WHERE name=%s',
                    (synonyms, category, name))
        conn.commit()


def delete_item(name):
    with conn.cursor() as cur:
        cur.execute('DELETE FROM items WHERE name=%s', (name,))
        conn.commit()


def write_items(data, date, supplier):
    cur = conn.cursor()
    for i in data:
        name = i[0]
        price = float(i[1])
        cur.execute("INSERT INTO items (name, date, price, supplier_name) VALUES (%s, %s, %s, %s)",
                    (name, date, price, supplier))
    conn.commit()


def write_import_items(name, categorie):
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name, date, category) VALUES (%s, NOW(), %s)", (name, categorie))
    cur.commit()


def write_import_synonyms(name, synonyms):
    cur = conn.cursor()
    cur.execute("UPDATE items SET synonyms = %s WHERE name=%s", (synonyms, name))
    cur.commit()


def get_items():
    cur = conn.cursor()
    cur.execute("SELECT * from items")
    rows = cur.fetchall()
    return rows
