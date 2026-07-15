
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "weather_history.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the search_history table if it doesn't already exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS search_history (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                city          TEXT NOT NULL,
                country       TEXT,
                temperature   REAL,
                humidity      INTEGER,
                description   TEXT,
                wind_speed    REAL,
                sunrise       TEXT,
                sunset        TEXT,
                searched_at   TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_search(city, country, temperature, humidity, description,
                 wind_speed, sunrise, sunset):
    """Insert one weather snapshot into the history table."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO search_history
                (city, country, temperature, humidity, description,
                 wind_speed, sunrise, sunset, searched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                city,
                country,
                temperature,
                humidity,
                description,
                wind_speed,
                sunrise,
                sunset,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()


def get_history(limit=50):
    """Return the most recent search records, newest first, as a list of dicts."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, city, country, temperature, humidity, description,
                   wind_speed, sunrise, sunset, searched_at
            FROM search_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]


def clear_history():
    """Delete every record from the history table."""
    with get_connection() as conn:
        conn.execute("DELETE FROM search_history")
        conn.commit()
