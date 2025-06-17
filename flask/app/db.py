import psycopg2
from psycopg2.extras import RealDictCursor

def get_conn():
    return psycopg2.connect(
        dbname='gpgeo',
        user='gpgeo_user',
        password='gpgeo_pass',
        host='db',
        port=5432,
        cursor_factory=RealDictCursor
    )
