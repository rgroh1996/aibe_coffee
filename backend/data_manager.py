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
        cur.execute("SELECT first_name, surname, debt FROM users")
        results = cur.fetchall()
        # Return in format (full_name, debt) for compatibility
        return [(f"{first_name} {surname}".strip(), debt) for first_name, surname, debt in results]
    
    def check_user_exists(self, first_name, surname):
        cur = self.db_conn.cursor()
        cur.execute("SELECT * FROM users WHERE first_name = ? AND surname = ?", (first_name, surname))
        return cur.fetchone()

    def check_user_exists_by_name(self, full_name):
        """Legacy method for backward compatibility"""
        name_parts = full_name.strip().split(' ', 1)
        first_name = name_parts[0]
        surname = name_parts[1] if len(name_parts) > 1 else ''
        return self.check_user_exists(first_name, surname)

    def add_new_user(self, first_name, surname):
        cur = self.db_conn.cursor()
        cur.execute("INSERT INTO users (first_name, surname, debt) VALUES (?, ?, ?)", (first_name, surname, 0))
        self.db_conn.commit()
        return cur.lastrowid

    def add_new_user_legacy(self, full_name):
        """Legacy method for backward compatibility"""
        name_parts = full_name.strip().split(' ', 1)
        first_name = name_parts[0]
        surname = name_parts[1] if len(name_parts) > 1 else ''
        return self.add_new_user(first_name, surname)

    def add_cleaning(self, user, product, total_price): 
        # change debt of user 
        cur = self.db_conn.cursor()
        cur.execute("INSERT INTO cleaning (user, cleaning_type, credit, time_stamp) VALUES (?, ?, ?, ?)", (user, product, -1 * total_price, datetime.now()))
        self.db_conn.commit()
        self._add_product_debt(user, total_price)

    def get_user_debt(self, user):
        cur = self.db_conn.cursor()
        # Support both new format (first_name, surname) and legacy format (full_name)
        if isinstance(user, tuple) and len(user) == 2:
            first_name, surname = user
            cur.execute("SELECT debt FROM users WHERE first_name = ? AND surname = ?", (first_name, surname))
        else:
            # Legacy support: try to match by full name
            name_parts = user.strip().split(' ', 1)
            first_name = name_parts[0]
            surname = name_parts[1] if len(name_parts) > 1 else ''
            cur.execute("SELECT debt FROM users WHERE first_name = ? AND surname = ?", (first_name, surname))
        result = cur.fetchone()
        return result[0] if result else 0
    
    def pay_debt(self, user, amount):
        self.update_user_debt(user, 0)
        
        cur = self.db_conn.cursor()
        cur.execute("INSERT INTO debt_paid (user, amount, time_stamp) VALUES (?, ?, ?)", (user, amount, datetime.now()))
        self.db_conn.commit()
    
    def update_user_debt(self, user, debt):
        cur = self.db_conn.cursor()
        # Support both new format (first_name, surname) and legacy format (full_name)
        if isinstance(user, tuple) and len(user) == 2:
            first_name, surname = user
            cur.execute("UPDATE users SET debt = ? WHERE first_name = ? AND surname = ?", (debt, first_name, surname))
        else:
            # Legacy support: try to match by full name
            name_parts = user.strip().split(' ', 1)
            first_name = name_parts[0]
            surname = name_parts[1] if len(name_parts) > 1 else ''
            cur.execute("UPDATE users SET debt = ? WHERE first_name = ? AND surname = ?", (debt, first_name, surname))
        self.db_conn.commit()
        
    def _add_product_debt(self, user, price):
        cur = self.db_conn.cursor()
        # Support both new format (first_name, surname) and legacy format (full_name)
        if isinstance(user, tuple) and len(user) == 2:
            first_name, surname = user
            cur.execute("SELECT debt FROM users WHERE first_name = ? AND surname = ?", (first_name, surname))
        else:
            # Legacy support: try to match by full name
            name_parts = user.strip().split(' ', 1)
            first_name = name_parts[0]
            surname = name_parts[1] if len(name_parts) > 1 else ''
            cur.execute("SELECT debt FROM users WHERE first_name = ? AND surname = ?", (first_name, surname))
        
        result = cur.fetchone()
        if result:
            debt = result[0]
            if isinstance(user, tuple) and len(user) == 2:
                cur.execute("UPDATE users SET debt = ? WHERE first_name = ? AND surname = ?", (debt + price, first_name, surname))
            else:
                cur.execute("UPDATE users SET debt = ? WHERE first_name = ? AND surname = ?", (debt + price, first_name, surname))
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