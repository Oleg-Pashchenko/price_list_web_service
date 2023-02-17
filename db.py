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


def write_items(data, date, supplier):
    cur = conn.cursor()
    for i in data:
        name = i[0]
        price = float(i[1])
        cur.execute("INSERT INTO items (name, date, price, supplier_name) VALUES (%s, %s, %s, %s)",
                    (name, date, price, supplier))
    conn.commit()