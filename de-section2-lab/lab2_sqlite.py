import sqlite3

# Membuat/Membuka database
conn = sqlite3.connect("store.db")
cur = conn.cursor()

# ======================
# CREATE TABLES
# ======================

cur.execute("""
CREATE TABLE IF NOT EXISTS customers(
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    qty INTEGER,
    order_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
)
""")

# ======================
# INSERT DATA
# ======================

cur.executemany(
    "INSERT OR IGNORE INTO customers VALUES (?, ?, ?)",
    [
        (1, "Alice", "alice@email.com"),
        (2, "Bob", "bob@email.com")
    ]
)

cur.executemany(
    "INSERT OR IGNORE INTO products VALUES (?, ?, ?)",
    [
        (1, "Laptop", 999.0),
        (2, "Mouse", 25.5),
        (3, "Keyboard", 49.9)
    ]
)

cur.executemany(
    "INSERT OR IGNORE INTO orders VALUES (?, ?, ?, ?, ?)",
    [
        (1, 1, 1, 1, "2024-01-01"),
        (2, 2, 2, 2, "2024-01-02")
    ]
)

conn.commit()

print("Data berhasil ditambahkan!")

print("\nAll Customers:")

for row in cur.execute(
    "SELECT * FROM customers"
):
    print(row)

print("\nCustomers + Orders + Products:")

for row in cur.execute("""
SELECT
    c.name,
    p.name,
    o.qty,
    (o.qty * p.price) AS total

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

JOIN products p
    ON o.product_id = p.product_id
"""):
    print(row)

conn.close()