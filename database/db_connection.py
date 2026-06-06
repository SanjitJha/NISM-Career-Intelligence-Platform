import mysql.connector
from mysql.connector import Error
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT


def get_connection():
    """Return a live MySQL connection. Raises on failure."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            autocommit=False,
        )
        return conn
    except Error as e:
        raise ConnectionError(f"[DB] Could not connect to MySQL: {e}")


def execute_query(query: str, params: tuple = None, fetch: bool = False):
    """
    Run a single query. Use fetch=True for SELECT.
    Returns rows list for SELECT, lastrowid for INSERT.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        conn.rollback()
        raise RuntimeError(f"[DB] Query failed: {e}\nQuery: {query}")
    finally:
        cursor.close()
        conn.close()


def execute_many(query: str, data: list):
    """Bulk insert using executemany — much faster than row-by-row inserts."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.executemany(query, data)
        conn.commit()
        return cursor.rowcount
    except Error as e:
        conn.rollback()
        raise RuntimeError(f"[DB] Bulk insert failed: {e}")
    finally:
        cursor.close()
        conn.close()


def test_connection():
    """Quick health check — prints OK or error."""
    try:
        conn = get_connection()
        print(f"✅  Connected to MySQL — database: {DB_NAME}")
        conn.close()
    except ConnectionError as e:
        print(f"❌  {e}")


if __name__ == "__main__":
    test_connection()
