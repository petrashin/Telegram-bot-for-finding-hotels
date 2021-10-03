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
        bot.send_message(message.from_user.id, "В каком городе будет производиться поиск?")
        bot.register_next_step_handler(message, get_city)
    else:
        bot.send_message(message.from_user.id, "Привет, чтобы получить информацию о командах, введи команду /help")
        bot.register_next_step_handler(message, help_func)


def help_func(message):
    if message.text == '/help':
        bot.send_message(message.from_user.id, "Это функция-помощник, но она сейчас недоступна")


def get_city(message):
    with open("info_from_user.txt", 'a', encoding='UTF-8') as f:
        f.write('1) {}'.format('{}\n'.format(message.text)))
    bot.send_message(message.from_user.id, "Какое количество отелей будем искать (максимум - {})?".format(
        MAX_HOTELS
    ))
    bot.register_next_step_handler(message, get_number_of_hotels)


def get_number_of_hotels(message):
    with open("info_from_user.txt", 'a', encoding='UTF-8') as f:
        f.write('2) {}'.format('{}\n'.format(message.text)))
    bot.send_message(message.from_user.id, "Нужно ли выводить фотографии отеля?")
    bot.register_next_step_handler(message, need_to_return_photos_func)


def need_to_return_photos_func(message):
    if message.text.lower() == 'да':
        with open("info_from_user.txt", 'a', encoding='UTF-8') as f:
            f.write('3) {}'.format('{}\n'.format(True)))
    elif message.text.lower == 'нет':
        with open("info_from_user.txt", 'a', encoding='UTF-8') as f:
            f.write('3) {}'.format('{}\n'.format(False)))
    bot.register_next_step_handler(message, lowprice_func)


def lowprice_func(message):
    with open("info_from_user.txt", 'r', encoding='UTT-8') as f:
        lines = f.readlines()
        city = lines[0][3:].strip('\n')
        number_of_hotels = int(lines[1][3:].strip('\n'))
        need_to_return_photos = bool(lines[2][3:].strip('\n'))

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'info_from_user.txt')
    os.remove(path)

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
