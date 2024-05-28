import sqlite3
from sqlite3 import Error

class DataManager:
    def __init__(self, db_file):

        # Initialize the connection to the database
        try:
            self.db_conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

    def load_users_and_debts(self):
        cur = self.db_conn.cursor()
        cur.execute("SELECT user, debt FROM users")
        return cur.fetchall()
    
    def check_user_exists(self, user):
        cur = self.db_conn.cursor()
        cur.execute("SELECT * FROM users WHERE user = ?", (user,))
        return cur.fetchone()

    def add_new_user(self, user):
        cur = self.db_conn.cursor()
        cur.execute("INSERT INTO users (user, debt) VALUES (?, ?)", (user, 0))
        self.db_conn.commit()
    
    def update_user_debt(self, user, debt):
        cur = self.db_conn.cursor()
        cur.execute("UPDATE users SET debt = ? WHERE user = ?", (debt, user))
        self.db_conn.commit()

    def add_consumed_product(self, user, product, sugar, milk):
        cur = self.db_conn.cursor()
        cur.execute("INSERT INTO consume (user, product, sugar, milk, time_stamp) VALUES (?, ?, ?, ?, datetime('now'))", (user, product, sugar, milk))
        self.db_conn.commit()