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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            first_name TEXT NOT NULL, 
            surname TEXT NOT NULL, 
            debt REAL,
            UNIQUE(first_name, surname)
        )
    """)
    cur.execute("CREATE TABLE IF NOT EXISTS consumed (id INTEGER PRIMARY KEY, user TEXT, product TEXT, options TEXT, price REAL, time_stamp TEXT, user_id INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS debt_paid (id INTEGER PRIMARY KEY, user TEXT, amount REAL, time_stamp TEXT, user_id INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS cleaning (id INTEGER PRIMARY KEY, user TEXT, cleaning_type TEXT, time_stamp TEXT, user_id INTEGER)")
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
    
    # Check if users table needs to be migrated to use first_name and surname
    cur.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cur.fetchall()]
    
    if 'first_name' not in columns:
        # Create new users table with separate name fields
        cur.execute("""
            CREATE TABLE users_new (
                id INTEGER PRIMARY KEY, 
                first_name TEXT NOT NULL, 
                surname TEXT NOT NULL, 
                debt REAL,
                UNIQUE(first_name, surname)
            )
        """)
        
        # Migrate existing data if any
        cur.execute("SELECT id, user, debt FROM users")
        existing_users = cur.fetchall()
        
        for user_id, full_name, debt in existing_users:
            # Split the full name into first and last name
            name_parts = full_name.strip().split(' ', 1)
            first_name = name_parts[0]
            surname = name_parts[1] if len(name_parts) > 1 else ''
            
            try:
                cur.execute(
                    "INSERT INTO users_new (id, first_name, surname, debt) VALUES (?, ?, ?, ?)",
                    (user_id, first_name, surname, debt)
                )
            except sqlite3.IntegrityError:
                # Handle duplicate names by appending a number
                counter = 1
                while True:
                    try:
                        modified_surname = f"{surname}_{counter}" if surname else f"_{counter}"
                        cur.execute(
                            "INSERT INTO users_new (id, first_name, surname, debt) VALUES (?, ?, ?, ?)",
                            (user_id, first_name, modified_surname, debt)
                        )
                        break
                    except sqlite3.IntegrityError:
                        counter += 1
        
        # Replace old table with new one
        cur.execute("DROP TABLE users")
        cur.execute("ALTER TABLE users_new RENAME TO users")
        
        # Update foreign key references in other tables
        # Update consumed table
        cur.execute("PRAGMA table_info(consumed)")
        consumed_columns = [column[1] for column in cur.fetchall()]
        if 'user_id' not in consumed_columns:
            cur.execute("ALTER TABLE consumed ADD COLUMN user_id INTEGER")
            # Update user_id based on matching names (this is best effort)
            cur.execute("""
                UPDATE consumed SET user_id = (
                    SELECT u.id FROM users u 
                    WHERE u.first_name || ' ' || u.surname = consumed.user
                    OR u.first_name = consumed.user
                )
            """)
        
        # Update debt_paid table
        cur.execute("PRAGMA table_info(debt_paid)")
        debt_paid_columns = [column[1] for column in cur.fetchall()]
        if 'user_id' not in debt_paid_columns:
            cur.execute("ALTER TABLE debt_paid ADD COLUMN user_id INTEGER")
            cur.execute("""
                UPDATE debt_paid SET user_id = (
                    SELECT u.id FROM users u 
                    WHERE u.first_name || ' ' || u.surname = debt_paid.user
                    OR u.first_name = debt_paid.user
                )
            """)
        
        # Update cleaning table
        cur.execute("PRAGMA table_info(cleaning)")
        cleaning_columns = [column[1] for column in cur.fetchall()]
        if 'user_id' not in cleaning_columns:
            cur.execute("ALTER TABLE cleaning ADD COLUMN user_id INTEGER")
            cur.execute("""
                UPDATE cleaning SET user_id = (
                    SELECT u.id FROM users u 
                    WHERE u.first_name || ' ' || u.surname = cleaning.user
                    OR u.first_name = cleaning.user
                )
            """)
        
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