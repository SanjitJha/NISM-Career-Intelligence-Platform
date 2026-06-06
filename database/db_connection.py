"""
database/db_connection.py
─────────────────────────
Reusable MySQL connector for the NISM Career Intelligence Platform.

Public API:
    get_connection()         → raw mysql.connector.connection
    execute_query()          → run SELECT (fetch=True) or DML
    execute_many()           → bulk INSERT/UPDATE
    fetch_dataframe()        → execute SELECT → pandas DataFrame
    test_connection()        → quick health-check printout
"""

import sys
import os
import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager

# allow imports from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT


# ─────────────────────────────────────────────────────────────────
# Connection pool config  (reuse connections instead of open/close)
# ─────────────────────────────────────────────────────────────────
_POOL_CONFIG = dict(
    host       = DB_HOST,
    user       = DB_USER,
    password   = DB_PASSWORD,
    database   = DB_NAME,
    port       = DB_PORT,
    charset    = "utf8mb4",
    autocommit = False,
)


def get_connection() -> mysql.connector.MySQLConnection:
    """
    Open and return a raw MySQL connection.
    The caller is responsible for closing it.
    Raises ConnectionError on failure.
    """
    try:
        conn = mysql.connector.connect(**_POOL_CONFIG)
        return conn
    except Error as e:
        raise ConnectionError(
            f"[DB] Cannot connect to MySQL at {DB_HOST}:{DB_PORT} "
            f"(database={DB_NAME}): {e}"
        )


@contextmanager
def managed_connection():
    """
    Context-manager wrapper — automatically closes the connection.

    Usage:
        with managed_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            ...
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────
# Core query helpers
# ─────────────────────────────────────────────────────────────────

def execute_query(
    query:  str,
    params: tuple | dict | None = None,
    fetch:  bool = False,
) -> list[dict] | int | None:
    """
    Run a single SQL statement.

    Parameters
    ----------
    query   : SQL string (use %s for positional or %(name)s for named params)
    params  : tuple, dict, or None
    fetch   : True  → returns list[dict] (SELECT)
              False → commits and returns lastrowid (INSERT/UPDATE/DELETE)

    Examples
    --------
    # SELECT
    rows = execute_query("SELECT * FROM jobs WHERE city=%s", ("Mumbai",), fetch=True)

    # INSERT
    new_id = execute_query("INSERT INTO jobs (...) VALUES (...)", {...})

    # UPDATE
    execute_query("UPDATE jobs SET is_active=0 WHERE job_id=%s", (42,))
    """
    with managed_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if fetch:
                return cursor.fetchall()
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            conn.rollback()
            raise RuntimeError(
                f"[DB] Query failed: {e}\n"
                f"Query : {query[:200]}\n"
                f"Params: {str(params)[:200]}"
            )
        finally:
            cursor.close()


def execute_many(query: str, data: list[tuple | dict]) -> int:
    """
    Bulk INSERT / UPDATE using executemany.
    ~10× faster than looping execute_query for large batches.

    Returns the number of rows affected.

    Example
    -------
    rows_affected = execute_many(
        "INSERT INTO jobs (company_name, position) VALUES (%s, %s)",
        [("HDFC AMC", "Advisor"), ("Zerodha", "Analyst")]
    )
    """
    if not data:
        return 0
    with managed_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.executemany(query, data)
            conn.commit()
            return cursor.rowcount
        except Error as e:
            conn.rollback()
            raise RuntimeError(f"[DB] Bulk operation failed: {e}")
        finally:
            cursor.close()


def fetch_dataframe(query: str, params: tuple | dict | None = None):
    """
    Execute a SELECT and return the result as a pandas DataFrame.
    Returns an empty DataFrame (not None) if the query returns no rows.

    Example
    -------
    df = fetch_dataframe(
        "SELECT city, COUNT(*) AS cnt FROM jobs GROUP BY city",
    )
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas is required for fetch_dataframe(). Run: pip install pandas")

    rows = execute_query(query, params, fetch=True)
    return pd.DataFrame(rows) if rows else pd.DataFrame()


# ─────────────────────────────────────────────────────────────────
# Health check
# ─────────────────────────────────────────────────────────────────

def test_connection() -> bool:
    """
    Quick health check. Prints a success or failure message.
    Returns True if connection is OK.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print(f"✅  MySQL {version}  |  database: {DB_NAME}  |  host: {DB_HOST}:{DB_PORT}")
        return True
    except (ConnectionError, Error) as e:
        print(f"❌  Connection failed: {e}")
        return False


if __name__ == "__main__":
    test_connection()
