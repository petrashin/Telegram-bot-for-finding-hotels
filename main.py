import os
import telebot
from dotenv import load_dotenv
from botrequests import lowprice
import sqlite3


conn = sqlite3.connect("history.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE history
                  (user_id text, command text,  city text, number_of_hotels text, need_photos text)""")

MAX_PHOTOS = 5
MAX_HOTELS = 5

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def start(message):
    command = message.text
    user_id = message.from_user.id
    if command == '/lowprice':
        bot.send_message(message.chat.id, "В каком городе будет производиться поиск?")
        bot.register_next_step_handler(message, get_city, user_id, command)
    elif command == '/help':
        bot.register_next_step_handler(message, help_func)
    else:
        bot.send_message(message.chat.id, "Привет, чтобы получить информацию о командах, введи команду /help")
        bot.register_next_step_handler(message, help_func)


def help_func(message):
    bot.send_message(message.chat.id, "Это функция-помощник, но она сейчас недоступна")


def get_city(message, user_id, command):
    city = message.text
    bot.send_message(message.chat.id, "Какое количество отелей будем искать (максимум - {})?".format(
        MAX_HOTELS
    ))
    bot.register_next_step_handler(message, get_number_of_hotels, user_id, command, city)


def get_number_of_hotels(message, user_id, command, city):
    number_of_hotels = int(message.text)
    bot.send_message(message.chat.id, "Нужно ли выводить фотографии отеля (максимум - {})?".format(
        MAX_PHOTOS
    ))
    bot.register_next_step_handler(message, need_to_return_photos_func, user_id, command, city, number_of_hotels)


def need_to_return_photos_func(message, user_id, command, city, number_of_hotels):
    if message.text.lower() == 'да':
        cursor.execute("""INSERT INTO history
                          VALUES ('{}', '{}', '{}', '{}', '{}') """.format(
            command,
            user_id,
            city,
            number_of_hotels,
            True
        ))
        conn.commit()
    elif message.text.lower() == 'нет':
        cursor.execute("""INSERT INTO history
                          VALUES ('{}', '{}', '{}', '{}', '{}') """.format(
            command,
            user_id,
            city,
            number_of_hotels,
            False
        ))
        conn.commit()
    bot.register_next_step_handler(message, lowprice_func)


def lowprice_func(message):
    sql = "SELECT city, number_of_hotels, need_photos FROM history"
    cursor.execute(sql)
    city, number_of_hotels, need_to_return_photos = list(*cursor.fetchall())

    result_of_search = lowprice.main(city, number_of_hotels, need_to_return_photos)

    for hotel in result_of_search:
        message = "Название отеля: {}\n" \
                  "Адрес отеля: {}\n" \
                  "Удаленность от центра: {}\n" \
                  "Цена: {}\n" \
                  "Ссылки на фотографии отеля: {}".format(
                    hotel["hotel_name"],
                    hotel["address"],
                    hotel["distance_to_center"],
                    hotel["price"],
                    hotel["hotel_photos"]
                    )
    bot.send_message(message.chat.id, message)
        

bot.polling(none_stop=True, interval=0)
