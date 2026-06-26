from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI(title="Order Management API")


DB_NAME = "orders.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        total_amount REAL NOT NULL,
        status TEXT NOT NULL,
        payment_status TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


init_db()


class OrderCreate(BaseModel):
    customer_name: str
    product_id: int
    product_name: str
    quantity: int
    price: float


@app.get("/")
def home():
    return {"message": "Order API running with SQLite"}


@app.post("/orders")
def create_order(order: OrderCreate):
    total = order.quantity * order.price

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO orders (
        customer_name,
        product_id,
        product_name,
        quantity,
        price,
        total_amount,
        status,
        payment_status,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        order.customer_name,
        order.product_id,
        order.product_name,
        order.quantity,
        order.price,
        total,
        "CREATED",
        "PENDING",
        datetime.now().isoformat()
    ))

    conn.commit()
    order_id = cursor.lastrowid
    conn.close()

    return {
        "message": "Order created successfully",
        "order_id": order_id,
        "total_amount": total,
        "status": "CREATED",
        "payment_status": "PENDING"
    }


@app.get("/orders")
def get_all_orders():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

@app.get("/orders/latest-order")
def get_latest_order():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
           
       customer_name,
        product_id,
        product_name,
        quantity,
        price,
        total_amount,
        status,
        payment_status,
        created_at
        FROM orders
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "No orders found"}

    return {
        "id": row[0],
        "customer_name": row[1],
        "customer_email": row[2],
        "product_id": row[3],
        "product_name": row[4],
        "quantity": row[5],
        "price": row[6],
        "total_amount": row[7],
        "status": row[8],
        "payment_status": row[9],
        "created_at": row[10]
    }
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return dict(row)


@app.put("/orders/{order_id}/pay")
def pay_order(order_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")

    cursor.execute("""
    UPDATE orders
    SET payment_status = ?, status = ?
    WHERE id = ?
    """, ("PAID", "CONFIRMED", order_id))

    conn.commit()
    conn.close()

    return {
        "message": "Payment completed",
        "order_id": order_id,
        "status": "CONFIRMED",
        "payment_status": "PAID"
    }


@app.put("/orders/{order_id}/cancel")
def cancel_order(order_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")

    cursor.execute("""
    UPDATE orders
    SET status = ?
    WHERE id = ?
    """, ("CANCELLED", order_id))

    conn.commit()
    conn.close()

    return {
        "message": "Order cancelled",
        "order_id": order_id,
        "status": "CANCELLED"
    }


@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")

    conn.close()

    return {"message": "Order deleted", "order_id": order_id}

