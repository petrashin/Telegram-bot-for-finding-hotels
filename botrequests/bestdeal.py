import requests
import json
from decouple import config
from typing import List, Dict

x_rapidapi_key = config('x_rapidapi_key')

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': x_rapidapi_key
    }


def get_destination_id(name_of_place: str) -> str:
    """
    Функция возвращающая destinationId города,
    название которого передано в данную функцию в качестве строки
    """
    url = "https://hotels4.p.rapidapi.com/locations/search"
    querystring = {"query": name_of_place, "locale": "en_US"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return data["suggestions"][0]["entities"][0]["destinationId"]


def get_urls_of_photos(hotel_id: str, number_of_photos: int) -> List[str]:
    """
    Функция, принимающая hotel_id и number_of_photos
    и возвращающая список url фотографий заданного отеля
    """
    list_of_photos = []
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel_id}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    for i in range(number_of_photos):
        url_of_photo = data["hotelImages"][i]["baseUrl"].replace('{size}', 'w')
        list_of_photos.append(url_of_photo)

    return list_of_photos


def get_all_info(dest_id: str,
                 number_of_hotels: int,
                 min_price: float,
                 max_price: float,
                 max_distance: float,
                 number_of_photos: int = 0) -> List[Dict[str, str]]:
    """
    Функция, принимающая dest_id, number_of_hotels и необязательный параметр number_of_photos.
    Возвращает список словарей, в котором хранится информация о каждом из отелей
    """

    result = []

    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": dest_id,
                   "pageNumber": "1",
                   "pageSize": "2500",
                   "checkIn": "2020-01-08",
                   "checkOut": "2020-01-15",
                   "adults1": "1",
                   "sortOrder": "PRICE",
                   "locale": "en_US",
                   "currency": "USD"
                   }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)

    counter = 0
    cur_index = 0
    while counter != number_of_hotels:
        new_data = {}

        try:

            hotel_id = data["data"]["body"]["searchResults"]["results"][cur_index]["id"]
            hotel_name = data["data"]["body"]["searchResults"]["results"][cur_index]["name"]
            address = data["data"]["body"]["searchResults"]["results"][cur_index]["address"]["streetAddress"]
            distance_to_center = data["data"]["body"]["searchResults"]["results"][cur_index]["landmarks"][0]["distance"]
            check_distance_to_center = float(distance_to_center[:distance_to_center.index('miles')])
            price = data["data"]["body"]["searchResults"]["results"][cur_index]["ratePlan"]["price"]["current"]
            check_price = float(price[1:])
            hotel_photos = get_urls_of_photos(hotel_id, number_of_photos)

            new_data['hotel_name'] = hotel_name
            new_data['address'] = address
            new_data['distance_to_center'] = distance_to_center
            new_data['price'] = price
            new_data['hotel_photos'] = hotel_photos

            if min_price <= check_price <= max_price and check_distance_to_center <= max_distance:
                result.append(new_data)
                counter += 1

        except KeyError:
            continue

        finally:
            cur_index += 1

    return result


def main(city_name: str,
         min_price: float,
         max_price: float,
         max_distance: float,
         number_of_hotels: int,
         need_to_return_photos: bool,
         number_of_photos: int) -> List[Dict[str, str]]:
    destination_id = get_destination_id(city_name)
    if need_to_return_photos:
        return get_all_info(destination_id,
                            number_of_hotels,
                            min_price,
                            max_price,
                            max_distance,
                            number_of_photos)
    else:
        return get_all_info(destination_id,
                            number_of_hotels,
                            min_price,
                            max_price,
                            max_distance)
