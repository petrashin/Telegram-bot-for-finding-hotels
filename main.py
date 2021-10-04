import os
import telebot
from dotenv import load_dotenv
from botrequests import lowprice


MAX_PHOTOS = 5
MAX_HOTELS = 10

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/lowprice':
        bot.send_message(message.chat.id, "В каком городе будет производиться поиск?")
        bot.register_next_step_handler(message, get_city)
    else:
        bot.send_message(message.chat.id, "Привет, чтобы получить информацию о командах, введи команду /help")
        bot.register_next_step_handler(message, help_func)


def help_func(message):
    if message.text == '/help':
        bot.send_message(message.chat.id, "Это функция-помощник, но она сейчас недоступна")


def get_city(message):
    searching_data = {'city': message.text}
    bot.send_message(message.chat.id, "Какое количество отелей будем искать (максимум - {})?".format(
        MAX_HOTELS
    ))
    bot.register_next_step_handler(message, get_number_of_hotels, searching_data)


def get_number_of_hotels(message, searching_data):
    searching_data['number_of_hotels'] = int(message.text)
    bot.send_message(message.chat.id, "Нужно ли выводить фотографии отеля?")
    bot.register_next_step_handler(message, need_to_return_photos_func, searching_data)


def need_to_return_photos_func(message, searching_data):
    if message.text.lower() == 'да':
        searching_data['need_to_return_photos'] = True
    elif message.text.lower() == 'нет':
        searching_data['need_to_return_photos'] = False
    bot.register_next_step_handler(message, lowprice_func, searching_data)


def lowprice_func(message, searching_data):
    result_of_search = lowprice.main(searching_data['city'],
                                     searching_data['number_of_hotels'],
                                     searching_data['need_to_return_photos'])

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
        print(message)
    bot.send_message(message.chat.id, message)
        

bot.polling(none_stop=True, interval=0)
