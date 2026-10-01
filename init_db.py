import sqlite3

conn = sqlite3.connect("flights.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    time TEXT NOT NULL,
    days TEXT NOT NULL
)
""")

flights = [
    ("LH400", "Frankfurt", "New York", "10:00-13:00", "Mo, Mi, Fr"),
    ("LH100", "Frankfurt", "London", "08:00-09:30", "täglich"),
    ("LH202", "Berlin", "Paris", "14:00-15:45", "Di, Do, Sa"),
]

cursor.executemany(
    "INSERT INTO flights (number, origin, destination, time, days) VALUES (?, ?, ?, ?, ?)",
    flights
)

conn.commit()
conn.close()
print("DB erstellt und befüllt.")
