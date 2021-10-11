import sqlite3


def create_table_of_data_base(data_base_name):
    conn = sqlite3.connect(data_base_name)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE history_of_searches
                      (user_id text, command text,  city text, number_of_hotels text, need_photos text)""")


def create_registration(data_base_name, user_id=None, command=None, city=None, number_of_hotels=None, need_to_return_photos=None):
    conn = sqlite3.connect(data_base_name)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO history
                      VALUES ('{}', '{}', '{}', '{}', '{}') """.format(
        user_id,
        command,
        city,
        number_of_hotels,
        need_to_return_photos
    ))
    conn.commit()


def get_info_from_data_base(data_base_name):
    conn = sqlite3.connect(data_base_name)
    cursor = conn.cursor()
    sql = "SELECT city, number_of_hotels, need_photos FROM history"
    cursor.execute(sql)
    city, number_of_hotels, need_to_return_photos = list(*cursor.fetchall())
    return city, number_of_hotels, need_to_return_photos

