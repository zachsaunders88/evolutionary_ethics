#!/usr/bin/env python3
"""
init_db.py

Initialize the SQLite database with the required tables:
- scenarios
- rules
- weights
- decisions
- fitness_logs
"""

import sqlite3

DB_PATH = 'data.db'


def init_db():
    conn = sqlite3.connect(DB_PATH)
    # Enable foreign key constraint support
    conn.execute("PRAGMA foreign_keys = ON;")
    c = conn.cursor()

    # Create scenarios table
    c.execute("""
    CREATE TABLE IF NOT EXISTS scenarios (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        code            TEXT    NOT NULL UNIQUE,
        owner_nearby    INTEGER NOT NULL,
        valuable        INTEGER NOT NULL,
        environment     TEXT    NOT NULL,
        legal_context   TEXT    NOT NULL
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS ga_runs (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        pop_size    INTEGER    NOT NULL,
        generations INTEGER    NOT NULL,
        cx_prob     REAL       NOT NULL,
        mut_prob    REAL       NOT NULL,
        run_time    DATETIME   DEFAULT CURRENT_TIMESTAMP
    )
    """)

    c.execute(""" 
    CREATE TABLE ga_generation_results (
        id            INTEGER PRIMARY KEY,
        run_id        INTEGER,
        generation    INTEGER,
        accuracy      REAL,
        util_weight   REAL,
        deon_weight   REAL,
        self_weight   REAL
    )
    """)

    c.execute("""
    CREATE TABLE ga_final_decisions (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id        INTEGER,
        scenario_code TEXT,
        action        TEXT,
        justification TEXT,
        score         REAL,
        FOREIGN KEY(run_id) REFERENCES ga_runs(id)
    )
    """)


    # Create rules table
    c.execute("""
    CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        params_json TEXT
    )
    """)
    # Insert default ethical rules
    c.executemany("""
    INSERT OR IGNORE INTO rules (name, description) VALUES (?, ?)
    """, [
        ('utilitarian', 'Maximize overall benefit'),
        ('deontological', 'Follow moral rules regardless of consequences'),
        ('self_interest', 'Prioritize self-benefit or minimal effort'),
    ])

    conn.commit()
    conn.close()
    print(f"Database initialized and tables created in '{DB_PATH}'.")

def test_db():
    """Test the database connection and table creation."""
    try:
        conn = sqlite3.connect(DB_PATH)
        # conn.execute("PRAGMA foreign_keys = ON;")
        c = conn.cursor()
        c.execute("""
            INSERT INTO rules (name, description, params_json)
            VALUES (?, ?, ?)
        """, ('fairness', 'Prioritize equitable outcomes', '{"threshold": 0.5}'))

        c.execute("""
            UPDATE rules
            SET description = ?
            WHERE name = ?
        """, ('Maximize overall well-being for the greatest number', 'utilitarian'))

        c.execute("""
            DELETE FROM rules
            WHERE name = ?
        """, ('self_interest',))

        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        print("Tables in the database:", tables)
        conn.commit()
        print("Database test completed successfully.")
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

if __name__ == '__main__':
    init_db()
    # test_db() # Test the database functionality
    # Uncomment the line below to initialize the database
