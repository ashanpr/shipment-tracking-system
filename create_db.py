import sqlite3

conn = sqlite3.connect('database.db')

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS shipments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tracking_number TEXT UNIQUE,
    status TEXT,
    location TEXT
)
""")

sample_shipments = [
    ('TRK001', 'In Transit', 'Colombo'),
    ('TRK002', 'Out for Delivery', 'Kandy'),
    ('TRK003', 'Delivered', 'Galle')
]

cursor.executemany("""
INSERT OR IGNORE INTO shipments
(tracking_number, status, location)
VALUES (?, ?, ?)
""", sample_shipments)

conn.commit()
conn.close()

print("Database created successfully.")