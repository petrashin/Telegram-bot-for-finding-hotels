import sqlite3
from datetime import datetime


def create():
    conn = sqlite3.connect("mydatabase.db", uri=True)
    cursor = conn.cursor()
    cursor.execute("""CREATE table IF NOT EXISTS history
                      (user_id text, command text, info_about_date text, search_result text);""")


def make_note(user_id, command, data):
    conn = sqlite3.connect("mydatabase.db", uri=True)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO history
                      VALUES ('{}', '{}', '{}', '{}')""".format(
        user_id,
        command,
        str(datetime.now())[:-7],
        data
    ))
    conn.commit()


def get_info(user_id):
    conn = sqlite3.connect("mydatabase.db", uri=True)
    cursor = conn.cursor()
    sql = "SELECT command, info_about_date, search_result FROM history WHERE user_id='{}'".format(user_id)
    cursor.execute(sql)

    return cursor.fetchall()
