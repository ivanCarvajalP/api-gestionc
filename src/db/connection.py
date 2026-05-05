import psycopg2
from psycopg2.extras import RealDictCursor
from src.core.config import settings

def get_connection():
    """
    Creates and returns a new database connection using psycopg2.
    Uses RealDictCursor so that results are returned as dictionaries.
    """
    conn = psycopg2.connect(
        settings.DATABASE_URL,
        cursor_factory=RealDictCursor
    )
    return conn
