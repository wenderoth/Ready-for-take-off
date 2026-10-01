import pytest
import sqlite3
import os
from project import format_flight_number, get_flight_by_number, get_all_flights


TEST_DB = "test_flights.db"


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Creates a small temporary test database before each test
    and deletes it afterward, so tests never touch flights.db.
    """
    conn = sqlite3.connect(TEST_DB)
    conn.execute("""
        CREATE TABLE flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            time TEXT NOT NULL,
            days TEXT NOT NULL
        )
    """)
    conn.execute(
        "INSERT INTO flights (number, origin, destination, time, days) VALUES (?, ?, ?, ?, ?)",
        ("LH400", "Frankfurt", "New York", "10:00-13:00", "Mo, Mi, Fr")
    )
    conn.commit()
    conn.close()

    yield

    os.remove(TEST_DB)


def test_format_flight_number():
    assert format_flight_number("lh400") == "LH400"
    assert format_flight_number("  lh100  ") == "LH100"
    with pytest.raises(ValueError):
        format_flight_number("")
    with pytest.raises(ValueError):
        format_flight_number("   ")


def test_get_flight_by_number():
    flight = get_flight_by_number("LH400", db_path=TEST_DB)
    assert flight is not None
    assert flight["origin"] == "Frankfurt"
    assert flight["destination"] == "New York"

    missing = get_flight_by_number("XX999", db_path=TEST_DB)
    assert missing is None


def test_get_all_flights():
    flights = get_all_flights(db_path=TEST_DB)
    assert len(flights) == 1
    assert flights[0]["number"] == "LH400"
