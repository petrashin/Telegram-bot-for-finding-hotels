import sqlite3
from datetime import datetime


def create():
    conn = sqlite3.connect("mydatabase.db", uri=True)
    cursor = conn.cursor()
    cursor.execute("""CREATE table IF NOT EXISTS history
                      (command text, info_about_date text, search_result text);""")


def make_note(command, data):
    conn = sqlite3.connect("mydatabase.db", uri=True)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO history
                      VALUES ('{}', '{}', '{}')""".format(
        command,
        str(datetime.now())[:-7],
        data
    ))
    conn.commit()


def get_info():
    conn = sqlite3.connect("mydatabase.db", uri=True)
    cursor = conn.cursor()
    sql = "SELECT * FROM history"
    cursor.execute(sql)

    return cursor.fetchall()
