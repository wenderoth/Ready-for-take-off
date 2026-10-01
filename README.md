CS50P Final Project
# ✈️ Ready for Take Off

#### Video Demo: <https://youtu.be/B3gm4by0PK8>

#### Description:

Ready for Take Off is a web application built with Flask and SQLite that allows users to search for flight information by entering a flight number, or browse a complete overview of all available flights.

The user enters a flight number (e.g. LH400) into a search form on the home page. The application queries a SQLite database and displays the route, departure and arrival times, and the days the flight operates. If the flight number is not found, the user receives a clear error message instead of a crash. A second page lists every flight currently stored in the database, giving users a way to browse instead of only searching.

## Features

- **Flight search** — enter a flight number and get the route, time, and operating days.
- **Flight overview** — a separate page (`/flights`) listing all flights stored in the database.
- **Case-insensitive input** — flight numbers are automatically converted to uppercase, so `lh400` and `LH400` both work.
- **Persistent storage** — flight data lives in a SQLite database (`flights.db`) instead of a hardcoded list, so it can be extended or queried independently of the app.

## How to Run

1. Install Flask:
   ```
   pip install flask
   ```

2. Create the database (only needed once, or whenever `flights.db` is missing/corrupted):
   ```
   python init_db.py
   ```

3. Start the application:
   ```
   python project.py
   ```

4. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## Project Structure

- `project.py` — Main Flask application: database connection, routes for search and overview
- `init_db.py` — One-time setup script that creates `flights.db` and inserts sample flight data
- `templates/index.html` — Search form (start page)
- `templates/result.html` — Displays the search result
- `templates/flights.html` — Displays all flights in the database
- `static/style.css` — Styling for the application

## Design Choices

Flight data was moved from a hardcoded Python list into a SQLite database. This was a deliberate step up from an earlier prototype: a list works for a handful of fixed entries, but a real database allows the flight data to grow, be queried directly (e.g. with the `sqlite3` CLI), and be reused by additional routes without touching the app logic itself.

The `.upper()` method on the search input ensures that users can enter flight numbers in lowercase (e.g. `lh400`) and still get a match, since flight numbers are stored uppercase in the database.

`sqlite3.Row` is used as the row factory so that query results can be accessed by column name (e.g. `flight["number"]`) in the templates, instead of relying on positional indexing.

## Challenges Faced

A few real bugs came up while building this that are worth mentioning, since they shaped some of the final design:

- **Duplicate routes:** while migrating from the list-based version to the database version, leftover code from the old version stayed in `app.py` alongside the new code, including two `if __name__ == "__main__":` blocks. Since Python executes top to bottom, the first `app.run()` call blocked execution before the rest of the file — including a new route — was ever read. This caused a confusing 404 for a route that "should" have existed. The fix was consolidating the file into a single, linear script with exactly one entry point at the end.
- **Corrupted database file:** `flights.db` is a binary file, not plain text. Opening it in a text editor (Notepad) and saving accidentally corrupted its internal structure, causing `sqlite3.DatabaseError: file is not a database`. The fix was deleting the corrupted file and regenerating it with `init_db.py` — and being more careful about which tools are safe to use on `.db` files going forward.

## Possible Future Improvements

- Add a booking feature (store a name + flight number in a separate table).
- Add user accounts / login.
- Replace the static sample data with a live flight API.
