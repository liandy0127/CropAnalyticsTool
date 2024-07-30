import psycopg2
from psycopg2 import OperationalError
from app import app

def get_db_conn():
    try:
        conn = psycopg2.connect(
            dbname=app.config['DB_NAME'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            host=app.config['DB_HOST'],
            port=app.config['DB_PORT']
        )
        return conn
    except OperationalError as e:
        print(f"Error: {e}")
        return None

def get_table_names():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'crops'")
    tables = cur.fetchall()
    cur.close()
    conn.close()
    return [table[0] for table in tables]

def export_table_to_csv(table_name, export_path):
    conn = get_db_conn()
    cur = conn.cursor()
    query = f"COPY (SELECT * FROM {table_name}) TO STDOUT WITH CSV HEADER"
    with open(export_path, 'w') as f:
        cur.copy_expert(query, f)
    cur.close()
    conn.close()
    return export_path
