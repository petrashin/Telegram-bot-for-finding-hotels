import os
import telebot
from dotenv import load_dotenv
from botrequests import lowprice, highprice, bestdeal, history

MAX_HOTELS = 5
MAX_PHOTOS = 5

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)


history.create()


@bot.message_handler(content_types=['text'])
def start(message: telebot.types.Message) -> None:
    command = message.text
    user_id = message.from_user.id
    if command == '/lowprice' or command == '/highprice' or command == '/bestdeal':
        bot.send_message(user_id, "Где будет производиться поиск? (прим. Moscow, Russia)?")
        bot.register_next_step_handler(message,
                                       get_city,
                                       user_id,
                                       command)
    elif command == '/help':
        bot.register_next_step_handler(message,
                                       help_func)
    elif command == '/history':
        bot.register_next_step_handler(message,
                                       get_history)
    else:
        bot.send_message(user_id, "Привет, чтобы получить информацию о командах, введи команду /help")
        bot.register_next_step_handler(message,
                                       help_func)


def get_history(message: telebot.types.Message) -> None:
    user_id = str(message.from_user.id)
    result = history.get_info(user_id)
    new_message = ''
    for line in result:
        new_message += "Использованная команда: {},\nДата и время использования: {},\nРезультат поиска: {}".format(
                line[0], line[1], line[2]
            ) + '\n\n'
    bot.send_message(user_id, new_message)


def help_func(message: telebot.types.Message) -> None:
    user_id = message.from_user.id
    bot.send_message(user_id, "Команды для поиска отелей:\n"
                              "/lowprice - Узнать топ самых дешёвых отелей в городе\n"
                              "/highprice - Узнать топ самых дорогих отелей в городе\n"
                              "/bestdeal - Узнать топ отелей, наиболее подходящих по цене и расположению от центра\n"
                              "/history - Узнать историю поиска отелей")


def get_city(message: telebot.types.Message, user_id: str, command: str) -> None:
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


def get_min_price(message: telebot.types.Message, user_id: str, command: str, city: str) -> None:
    min_price = float(message.text)
    bot.send_message(user_id, "Какова должна быть максимальная цена отеля в $?")
    bot.register_next_step_handler(message,
                                   get_max_price,
                                   user_id,
                                   command,
                                   city,
                                   min_price)


def get_max_price(message: telebot.types.Message, user_id: str, command: str, city: str, min_price: float) -> None:
    max_price = float(message.text)
    bot.send_message(user_id, "На каком наибольшем расстоянии от центра должен находиться отель в милях?")
    bot.register_next_step_handler(message,
                                   get_distance,
                                   user_id,
                                   command,
                                   city,
                                   min_price,
                                   max_price)


def get_distance(message: telebot.types.Message,
                 user_id: str,
                 command: str,
                 city: str,
                 min_price: float,
                 max_price: float):
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


def get_number_of_hotels(message: telebot.types.Message,
                         user_id: str,
                         command: str,
                         city: str,
                         min_price: float = None,
                         max_price: float = None,
                         max_distance: float = None):

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


def need_to_return_photos_func(message: telebot.types.Message,
                               user_id: str,
                               command: str,
                               city: str,
                               number_of_hotels: int,
                               min_price: float = None,
                               max_price: float = None,
                               max_distance: float = None):

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


def get_number_of_photos(message: telebot.types.Message,
                         user_id: str,
                         command: str,
                         city: str,
                         number_of_hotels: int,
                         need_to_return_photos: bool,
                         min_price: float = None,
                         max_price: float = None,
                         max_distance: float = None):

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

        hotels_found = []

        for hotel in result_of_search:
            hotels_found.append(hotel["hotel_name"])
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

        history.make_note(user_id, command, ', '.join(hotels_found))

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
