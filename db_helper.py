import mysql.connector

# Change this config as needed
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # or 'yourpassword'
        port =3308,
    )

def get_databases():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    dbs = [db[0] for db in cursor.fetchall()]
    conn.close()
    return dbs

def create_database(db_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
    conn.commit()
    conn.close()

def get_tables(db_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"USE `{db_name}`")
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    conn.close()
    return tables

def drop_table(database, table):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"USE `{database}`")
    cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
    conn.commit()
    conn.close()

def drop_database(database):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS `{database}`")
    conn.commit()
    conn.close()
