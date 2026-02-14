"""
Benchmark: measures query time for get_users_recently_consumed and
get_recent_cleanings with and without indexes, across growing data sizes.
"""

import sqlite3
import time
import random
import string
from datetime import datetime, timedelta


NUM_USERS = 50
ENTRY_COUNTS = [500, 2_000, 10_000, 50_000]
PRODUCTS = ["Espresso", "Cappuccino", "Latte", "Americano"]
CLEANING_TYPES = ["Descaling", "Side Compartment Cleaning", "Dishwasher ausräumen"]

INDEX_STMTS = [
    "CREATE INDEX IF NOT EXISTS idx_consumed_user_timestamp ON consumed (user, time_stamp)",
    "CREATE INDEX IF NOT EXISTS idx_cleaning_timestamp ON cleaning (time_stamp)",
]


def random_username():
    return "".join(random.choices(string.ascii_lowercase, k=6))


def create_tables(conn):
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user TEXT, debt REAL)")
    cur.execute("CREATE TABLE IF NOT EXISTS consumed (id INTEGER PRIMARY KEY, user TEXT, product TEXT, options TEXT, price REAL, time_stamp TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS cleaning (id INTEGER PRIMARY KEY, user TEXT, cleaning_type TEXT, credit REAL, time_stamp TEXT)")
    conn.commit()


def drop_indexes(conn):
    conn.execute("DROP INDEX IF EXISTS idx_consumed_user_timestamp")
    conn.execute("DROP INDEX IF EXISTS idx_cleaning_timestamp")
    conn.commit()


def create_indexes(conn):
    for stmt in INDEX_STMTS:
        conn.execute(stmt)
    conn.commit()


def populate(conn, users, n_consumed, n_cleaning):
    """Insert n_consumed rows into consumed and n_cleaning rows into cleaning."""
    now = datetime.now()
    cur = conn.cursor()

    consumed_rows = []
    for _ in range(n_consumed):
        user = random.choice(users)
        product = random.choice(PRODUCTS)
        price = round(random.uniform(0.3, 3.0), 2)
        # spread timestamps over the last 30 days so only ~half fall in the 2-week window
        ts = now - timedelta(seconds=random.randint(0, 30 * 86400))
        consumed_rows.append((user, product, "", price, str(ts)))
    cur.executemany(
        "INSERT INTO consumed (user, product, options, price, time_stamp) VALUES (?, ?, ?, ?, ?)",
        consumed_rows,
    )

    cleaning_rows = []
    for _ in range(n_cleaning):
        user = random.choice(users)
        ctype = random.choice(CLEANING_TYPES)
        credit = round(random.uniform(0.3, 1.5), 2)
        ts = now - timedelta(seconds=random.randint(0, 30 * 86400))
        cleaning_rows.append((user, ctype, credit, str(ts)))
    cur.executemany(
        "INSERT INTO cleaning (user, cleaning_type, credit, time_stamp) VALUES (?, ?, ?, ?)",
        cleaning_rows,
    )
    conn.commit()


def run_queries(conn):
    """Run the same queries the app runs on the main screen and return elapsed ms."""
    two_weeks_ago = datetime.now() - timedelta(weeks=2)

    t0 = time.perf_counter()
    conn.execute(
        """
        SELECT u.user,
               COALESCE(SUM(c.price), 0) AS total_consumed,
               u.debt AS debt_amount
        FROM users u
        LEFT JOIN consumed c ON u.user = c.user AND c.time_stamp >= ?
        GROUP BY u.user, u.debt
        """,
        (str(two_weeks_ago),),
    ).fetchall()

    conn.execute(
        """
        SELECT user, cleaning_type, credit
        FROM cleaning
        WHERE time_stamp >= ?
        """,
        (str(two_weeks_ago),),
    ).fetchall()
    elapsed = (time.perf_counter() - t0) * 1000
    return elapsed


def bench_size(n_entries, users):
    """Benchmark one data-size point, returning (no_index_ms, with_index_ms)."""
    conn = sqlite3.connect(":memory:")
    create_tables(conn)

    # insert users
    cur = conn.cursor()
    for u in users:
        cur.execute("INSERT INTO users (user, debt) VALUES (?, ?)", (u, round(random.uniform(0, 10), 2)))
    conn.commit()

    n_cleaning = max(1, n_entries // 5)
    populate(conn, users, n_entries, n_cleaning)

    # --- without indexes ---
    drop_indexes(conn)
    # warm up
    run_queries(conn)
    no_idx = min(run_queries(conn) for _ in range(5))

    # --- with indexes ---
    create_indexes(conn)
    # warm up
    run_queries(conn)
    with_idx = min(run_queries(conn) for _ in range(5))

    conn.close()
    return no_idx, with_idx


def main():
    users = [random_username() for _ in range(NUM_USERS)]

    print(f"{'Entries':>10}  {'No Index':>12}  {'With Index':>12}  {'Speedup':>8}")
    print("-" * 50)

    for n in ENTRY_COUNTS:
        no_idx, with_idx = bench_size(n, users)
        speedup = no_idx / with_idx if with_idx > 0 else float("inf")
        print(f"{n:>10,}  {no_idx:>10.2f}ms  {with_idx:>10.2f}ms  {speedup:>7.1f}x")


if __name__ == "__main__":
    main()
