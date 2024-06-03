import sqlite3
import pandas as pd

PATH = "../database/aibe_coffee.db"

conn = sqlite3.connect(PATH)
cur = conn.cursor()

users = pd.read_sql_query("SELECT * FROM users", conn)
print("\nUSERS: \n", users)

consumed_products = pd.read_sql_query("SELECT * FROM consumed", conn)
print("\nCONSUMED PRODUCTS: \n", consumed_products)

paid_debts = pd.read_sql_query("SELECT * FROM debt_paid", conn)
print("\nPAID DEBTS: \n", paid_debts)