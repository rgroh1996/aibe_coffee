import sqlite3
from sqlite3 import Error
from datetime import datetime
import os
import glob


def create_connection(db_file):
    """
    Create a database connection to the SQLite database
    """
    db_conn = None
    try:
        db_conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return db_conn

def init_table(db_conn):
    """ 
    Initialize the database with the necessary tables
    """
    cur = db_conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user TEXT, debt REAL)")
    cur.execute("CREATE TABLE IF NOT EXISTS consumed (id INTEGER PRIMARY KEY, user TEXT, product TEXT, options TEXT, price REAL, time_stamp TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS debt_paid (id INTEGER PRIMARY KEY, user TEXT, amount REAL, time_stamp TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS cleaning (id INTEGER PRIMARY KEY, user TEXT, cleaning_type TEXT, time_stamp TEXT)")
    db_conn.commit()

def migrate_database(db_conn):
    """
    Migrate the database to include new tables or columns without deleting existing data
    """
    cur = db_conn.cursor()
    # Check if the cleaning table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cleaning'")
    if not cur.fetchone():
        cur.execute("CREATE TABLE cleaning (id INTEGER PRIMARY KEY, user TEXT, cleaning_type TEXT, credit REAL, time_stamp TEXT)")
        db_conn.commit()


if __name__ == '__main__':

    database_path = "../database"
    # check if exists, otherwise create
    if not os.path.exists(database_path):
        os.makedirs(database_path)

    database_path = os.path.join(database_path, "aibe_coffee.db")

    # create a database connection
    conn = create_connection(database_path)
    with conn:
        migrate_database(conn)
        # create tables
        init_table(conn)