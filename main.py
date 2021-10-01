import os
import telebot
from dotenv import load_dotenv
from botrequests import lowprice


MAX_PHOTOS = 5
MAX_HOTELS = 10

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

city = ''
number_of_hotels = 0
need_to_return_photos = False
command = ''


@bot.message_handler(content_types=['text'])
def start(message):
    global command
    if message.text == '/lowprice':
        bot.send_message(message.from_user.id, "В каком городе будет производиться поиск?")
        bot.register_next_step_handler(message, get_city)
    else:
        bot.send_message(message.from_user.id, "Привет, чтобы получить информацию о командах, введи команду /help")
        bot.register_next_step_handler(message, help_func)


def help_func(message):
    if message.text == '/help':
        bot.send_message(message.from_user.id, "Это функция-помощник, но она сейчас недоступна")


def get_city(message):
    global city
    city = message.text
    bot.send_message(message.from_user.id, "Какое количество отелей будем искать (максимум - {})?".format(
        MAX_HOTELS
    ))
    bot.register_next_step_handler(message, get_number_of_hotels)


def get_number_of_hotels(message):
    global number_of_hotels
    number_of_hotels = int(message.text)
    bot.send_message(message.from_user.id, "Нужно ли выводить фотографии отеля?")
    bot.register_next_step_handler(message, need_to_return_photos_func)


def need_to_return_photos_func(message):
    global need_to_return_photos
    if message.text.lower() == 'да':
        need_to_return_photos = True
    elif message.text.lower == 'нет':
        need_to_return_photos = False
    bot.register_next_step_handler(message, lowprice_func)


def lowprice_func(message):
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
        bot.send_message(message.from_user.id, message)
        

bot.polling(none_stop=True, interval=0)
