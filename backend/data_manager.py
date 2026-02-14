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

        self._migrate_profile_columns()

    def _migrate_profile_columns(self):
        cur = self.db_conn.cursor()
        for col in ['first_name', 'last_name', 'lab']:
            try:
                cur.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT")
            except Exception:
                pass  # column already exists
        self.db_conn.commit()

    def load_users_and_debts(self):
        cur = self.db_conn.cursor()
        cur.execute("SELECT user, debt FROM users")
        return cur.fetchall()
    
    def check_user_exists(self, first_name, last_name):
        cur = self.db_conn.cursor()
        cur.execute("SELECT * FROM users WHERE first_name = ? AND last_name = ?", (first_name, last_name))
        return cur.fetchone()

    def add_new_user(self, first_name, last_name, lab):
        display_name = f"{first_name} {last_name}"
        cur = self.db_conn.cursor()
        cur.execute("INSERT INTO users (user, debt, first_name, last_name, lab) VALUES (?, ?, ?, ?, ?)",
                    (display_name, 0, first_name, last_name, lab))
        self.db_conn.commit()

    def is_profile_complete(self, user):
        cur = self.db_conn.cursor()
        cur.execute("SELECT first_name, last_name, lab FROM users WHERE user = ?", (user,))
        row = cur.fetchone()
        if not row:
            return False
        return all(val is not None for val in row)

    def complete_profile(self, old_username, first_name, last_name, lab):
        new_name = f"{first_name} {last_name}"
        cur = self.db_conn.cursor()
        try:
            cur.execute("UPDATE users SET user = ?, first_name = ?, last_name = ?, lab = ? WHERE user = ?",
                        (new_name, first_name, last_name, lab, old_username))
            cur.execute("UPDATE consumed SET user = ? WHERE user = ?", (new_name, old_username))
            cur.execute("UPDATE cleaning SET user = ? WHERE user = ?", (new_name, old_username))
            cur.execute("UPDATE debt_paid SET user = ? WHERE user = ?", (new_name, old_username))
            self.db_conn.commit()
        except Exception:
            self.db_conn.rollback()
            raise

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
                u.debt AS debt_amount,
                u.lab
            FROM users u
            LEFT JOIN consumed c ON u.user = c.user AND c.time_stamp >= ?
            GROUP BY u.user, u.debt, u.lab
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