import sqlite3
from sqlite3 import Error
from datetime import datetime, timedelta

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

    def add_cleaning(self, user, product, total_price): 
        # change debt of user 
        cur = self.db_conn.cursor()
        cur.execute("INSERT INTO cleaning (user, cleaning_type, credit, time_stamp) VALUES (?, ?, ?, ?)", (user, product, -1 * total_price, datetime.now()))
        self.db_conn.commit()
        self._add_product_debt(user, total_price)

    def get_user_debt(self, user):
        cur = self.db_conn.cursor()
        cur.execute("SELECT debt FROM users WHERE user = ?", (user,))
        return cur.fetchone()[0]
    
    def pay_debt(self, user, amount):
        self.update_user_debt(user, 0)
        
        cur = self.db_conn.cursor()
        cur.execute("INSERT INTO debt_paid (user, amount, time_stamp) VALUES (?, ?, ?)", (user, amount, datetime.now()))
        self.db_conn.commit()
    
    def update_user_debt(self, user, debt):
        cur = self.db_conn.cursor()
        cur.execute("UPDATE users SET debt = ? WHERE user = ?", (debt, user))
        self.db_conn.commit()
        
    def _add_product_debt(self, user, price):
        cur = self.db_conn.cursor()
        cur.execute("SELECT debt FROM users WHERE user = ?", (user,))
        debt = cur.fetchone()[0]
        cur.execute("UPDATE users SET debt = ? WHERE user = ?", (debt + price, user))
        self.db_conn.commit()

    def add_consumed_product(self, user, product, selected_options, total_price):
        cur = self.db_conn.cursor()
        cur.execute("INSERT INTO consumed (user, product, options, price, time_stamp) VALUES (?, ?, ?, ?, ?)", (user, product, selected_options, total_price, datetime.now()))
        self.db_conn.commit()
        
        self._add_product_debt(user, total_price)

    def get_users_recently_consumed(self):
        two_weeks_ago = datetime.now() - timedelta(weeks=2)
        cur = self.db_conn.cursor()
        cur.execute("""
            SELECT u.user, 
                COALESCE(SUM(c.price), 0) AS total_consumed, 
                u.debt AS debt_amount
            FROM users u
            LEFT JOIN consumed c ON u.user = c.user AND c.time_stamp >= ?
            GROUP BY u.user, u.debt
        """, (two_weeks_ago,))
        return cur.fetchall()

    def get_recent_cleanings(self):
        two_weeks_ago = datetime.now() - timedelta(weeks=2)
        cur = self.db_conn.cursor()
        cur.execute("""
            SELECT user, cleaning_type, credit 
            FROM cleaning
            WHERE time_stamp >= ?
        """, (two_weeks_ago,))
        return cur.fetchall()

    def get_cleanings_in_current_window(self, product, time_window):
        cutoff_date = datetime.now() - timedelta(days=time_window)
        cur = self.db_conn.cursor()
        cur.execute("""
            SELECT user, cleaning_type, credit, time_stamp
            FROM cleaning
            WHERE cleaning_type = ? AND time_stamp >= ?
        """, (product, cutoff_date))
        return cur.fetchall()