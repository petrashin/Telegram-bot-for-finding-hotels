import os
import telebot
from dotenv import load_dotenv
from botrequests import lowprice, highprice

MAX_HOTELS = 5
MAX_PHOTOS = 5

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def start(message):
    command = message.text
    user_id = message.from_user.id
    if command == '/lowprice' or command == '/highprice':
        bot.send_message(user_id, "Где будет производиться поиск? (прим. Moscow, Russia)?")
        bot.register_next_step_handler(message,
                                       get_city,
                                       user_id,
                                       command)
    elif command == '/help':
        bot.register_next_step_handler(user_id,
                                       help_func)
    else:
        bot.send_message(user_id, "Привет, чтобы получить информацию о командах, введи команду /help")
        bot.register_next_step_handler(message,
                                       help_func)


def help_func(message):
    bot.send_message(message.from_user.id, """
    Команды для поиска отелей:
    /lowprice - поиск дешёвых отелей
    /highprice - поиск дорогих отелей
    """)


def get_city(message, user_id, command):
    city = message.text
    bot.send_message(user_id, "Какое количество отелей будем искать (максимум - {})?".format(
        MAX_HOTELS
    ))
    bot.register_next_step_handler(message,
                                   get_number_of_hotels,
                                   user_id,
                                   command,
                                   city)


def get_number_of_hotels(message, user_id, command, city):
    number_of_hotels = int(message.text)
    if 1 <= number_of_hotels <= MAX_HOTELS:
        bot.send_message(user_id, "Нужно ли выводить фотографии отеля (да/нет)?")
        bot.register_next_step_handler(message,
                                       need_to_return_photos_func,
                                       user_id,
                                       command,
                                       city,
                                       number_of_hotels)
    else:
        bot.send_message(user_id, "Вы ввели неправильное количество отелей, попробуйте снова")
        bot.register_next_step_handler(message,
                                       get_number_of_hotels,
                                       user_id,
                                       command,
                                       city)


def need_to_return_photos_func(message, user_id, command, city, number_of_hotels):
    if message.text.lower() == 'да':
        need_to_return_photos = True
    else:
        need_to_return_photos = True

    bot.send_message(user_id, "Какое количество фотографий будем выводить (максимум - {})?".format(
        MAX_PHOTOS
    ))
    bot.register_next_step_handler(message,
                                   get_number_of_photos,
                                   user_id,
                                   command,
                                   city,
                                   number_of_hotels,
                                   need_to_return_photos)


def get_number_of_photos(message, user_id, command, city, number_of_hotels, need_to_return_photos):
    number_of_photos = int(message.text)
    if 1 <= number_of_photos <= MAX_PHOTOS:
        if command == '/lowprice':
            result_of_search = lowprice.main(city, number_of_hotels, need_to_return_photos, number_of_photos)
        elif command == '/highprice':
            result_of_search = highprice.main(city, number_of_hotels, need_to_return_photos, number_of_photos)
        else:
            result_of_search = {}

        for hotel in result_of_search:
            message = "Название отеля: {}\n" \
                      "Адрес отеля: {}\n" \
                      "Удаленность от центра: {}\n" \
                      "Цена: {}\n".format(
                    hotel["hotel_name"],
                    hotel["address"],
                    hotel["distance_to_center"],
                    hotel["price"],
                )
            bot.send_message(user_id, message)
            for photo in hotel["hotel_photos"]:
                bot.send_photo(user_id, photo)
    else:
        bot.send_message(user_id, "Вы ввели неправильное количество фотографий, попробуйте снова")
        bot.register_next_step_handler(message,
                                       get_number_of_photos,
                                       user_id,
                                       command,
                                       city,
                                       number_of_hotels,
                                       need_to_return_photos)


bot.polling(none_stop=True, interval=0)
