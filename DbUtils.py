import sqlite3
from typing import Tuple


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


def setup_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs_listings(
    job_id TEXT PRIMARY KEY,
    job_title TEXT NOT NULL,
    company_name TEXT NOT NULL,
    job_description TEXT DEFAULT "",
    location TEXT NOT NULL,
    min_salary INT DEFAULT 0,
    max_salary INT DEFAULT 0,
    salary_time TEXT DEFAULT "yearly",
    posted_at TEXT,
    url TEXT NOT NULL,
    remote BOOLEAN NOT NULL);''')


def insert_job(cursor: sqlite3.Cursor, job_tuple: Tuple):
    statement = '''INSERT OR IGNORE INTO jobs_listings
    (job_id, job_title, company_name, job_description, location, min_salary, max_salary, salary_time,
    posted_at, url, remote) VALUES (?, ?, ?,?,?,?,?,?,?,?, ?);'''
    cursor.execute(statement, job_tuple)


def save_to_db(cursor: sqlite3.Cursor, all_jobs: list[Tuple]):
    for job in all_jobs:
        try:
            insert_job(cursor, job)
        except sqlite3.IntegrityError:
            print(f"error inserting job with title {job[0]} its already there")
        except sqlite3.OperationalError as e:
            print(f"error inserting job {e}")
