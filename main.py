import os
import telebot
from dotenv import load_dotenv
from botrequests import lowprice
import databasefile


MAX_PHOTOS = 5
MAX_HOTELS = 5

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

databasefile.create_table_of_data_base("history.db")


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
        databasefile.create_registration("history.db", user_id, command, city, number_of_hotels, True)
    elif message.text.lower() == 'нет':
        databasefile.create_registration("history.db", user_id, command, city, number_of_hotels, False)
    bot.register_next_step_handler(message, lowprice_func)


def lowprice_func(message):
    city, number_of_hotels, need_to_return_photos = databasefile.get_info_from_data_base("history.db")
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
