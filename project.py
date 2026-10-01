from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


def format_flight_number(raw_input):
    """
    Normalizes user input into a flight number format.
    Strips whitespace and converts to uppercase.
    Raises ValueError if input is empty.
    """
    if not raw_input or not raw_input.strip():
        raise ValueError("Flight number cannot be empty")
    return raw_input.strip().upper()


def get_flight_by_number(flight_number, db_path="flights.db"):
    """
    Looks up a single flight by its flight number in the database.
    Returns a dict-like sqlite3.Row if found, otherwise None.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    flight = conn.execute(
        "SELECT * FROM flights WHERE number = ?", (flight_number,)
    ).fetchone()
    conn.close()
    return flight


def get_all_flights(db_path="flights.db"):
    """
    Returns a list of all flights stored in the database.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    flights = conn.execute("SELECT * FROM flights").fetchall()
    conn.close()
    return flights


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    try:
        flight_number = format_flight_number(request.form.get("flightnumber"))
    except ValueError:
        return render_template("result.html", flight=None, flightnumber="")

    flight = get_flight_by_number(flight_number)
    return render_template("result.html", flight=flight, flightnumber=flight_number)

@app.route("/flights")
def all_flights():
    flights = get_all_flights()
    return render_template("flights.html", flights=flights)


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
