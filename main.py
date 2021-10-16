import os
import telebot
from dotenv import load_dotenv
from botrequests import lowprice, highprice, bestdeal

MAX_HOTELS = 5
MAX_PHOTOS = 5

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def start(message):
    command = message.text
    user_id = message.from_user.id
    if command == '/lowprice' or command == '/highprice' or command == '/bestdeal':
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
    /lowprice - Узнать топ самых дешёвых отелей в городе
    /highprice - Узнать топ самых дорогих отелей в городе
    /bestdeal - Узнать топ отелей, наиболее подходящих по цене и расположению от центра
    """)


def get_city(message, user_id, command):
    city = message.text
    if command == '/lowprice' or command == '/highprice':
        bot.send_message(user_id, "Какое количество отелей будем искать (максимум - {})?".format(
            MAX_HOTELS
        ))
        bot.register_next_step_handler(message,
                                       get_number_of_hotels,
                                       user_id,
                                       command,
                                       city)
    elif command == '/bestdeal':
        bot.send_message(user_id, "Какова должна быть минимальная цена отеля в $?")
        bot.register_next_step_handler(message,
                                       get_min_price,
                                       user_id,
                                       command,
                                       city)


def get_min_price(message, user_id, command, city):
    min_price = float(message.text)
    bot.send_message(user_id, "Какова должна быть максимальная цена отеля в $?")
    bot.register_next_step_handler(message,
                                   get_max_price,
                                   user_id,
                                   command,
                                   city,
                                   min_price)


def get_max_price(message, user_id, command, city, min_price):
    max_price = float(message.text)
    bot.send_message(user_id, "На каком наибольшем расстоянии от центра должен находиться отель в милях?")
    bot.register_next_step_handler(message,
                                   get_distance,
                                   user_id,
                                   command,
                                   city,
                                   min_price,
                                   max_price)


def get_distance(message, user_id, command, city, min_price, max_price):
    max_distance = float(message.text)
    bot.send_message(user_id, "Какое количество отелей будем искать (максимум - {})?".format(
        MAX_HOTELS
    ))
    bot.register_next_step_handler(message,
                                   get_number_of_hotels,
                                   user_id,
                                   command,
                                   city,
                                   min_price,
                                   max_price,
                                   max_distance)


def get_number_of_hotels(message,
                         user_id,
                         command,
                         city,
                         min_price=None,
                         max_price=None,
                         max_distance=None):

    number_of_hotels = int(message.text)
    if 1 <= number_of_hotels <= MAX_HOTELS:
        bot.send_message(user_id, "Нужно ли выводить фотографии отеля (Да/Нет)?")
        bot.register_next_step_handler(message,
                                       need_to_return_photos_func,
                                       user_id,
                                       command,
                                       city,
                                       number_of_hotels,
                                       min_price,
                                       max_price,
                                       max_distance)
    else:
        bot.send_message(user_id, "Вы ввели неправильное количество отелей, попробуйте снова")
        bot.register_next_step_handler(message,
                                       get_number_of_hotels,
                                       user_id,
                                       command,
                                       city,
                                       min_price,
                                       max_price,
                                       max_distance)


def need_to_return_photos_func(message,
                               user_id,
                               command,
                               city,
                               number_of_hotels,
                               min_price=None,
                               max_price=None,
                               max_distance=None):

    if message.text.lower() == 'да':
        need_to_return_photos = True
    else:
        need_to_return_photos = False

    bot.send_message(user_id, "Какое количество фотографий будем выводить (максимум - {})?".format(
        MAX_PHOTOS
    ))
    bot.register_next_step_handler(message,
                                   get_number_of_photos,
                                   user_id,
                                   command,
                                   city,
                                   number_of_hotels,
                                   need_to_return_photos,
                                   min_price,
                                   max_price,
                                   max_distance)


def get_number_of_photos(message,
                         user_id,
                         command,
                         city,
                         number_of_hotels,
                         need_to_return_photos,
                         min_price=None,
                         max_price=None,
                         max_distance=None):

    number_of_photos = int(message.text)
    if 1 <= number_of_photos <= MAX_PHOTOS:
        if command == '/lowprice':
            result_of_search = lowprice.main(city,
                                             number_of_hotels,
                                             need_to_return_photos,
                                             number_of_photos)
        elif command == '/highprice':
            result_of_search = highprice.main(city,
                                              number_of_hotels,
                                              need_to_return_photos,
                                              number_of_photos)
        elif command == '/bestdeal':
            result_of_search = bestdeal.main(city,
                                             min_price,
                                             max_price,
                                             max_distance,
                                             number_of_hotels,
                                             need_to_return_photos,
                                             number_of_photos)
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
