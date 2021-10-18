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


def get_all_info(dest_id: str, number_of_hotels: int, number_of_photos: int = 0) -> List[Dict[str, str]]:
    """
    Функция, принимающая dest_id, number_of_hotels и необязательный параметр number_of_photos.
    Возвращает список словарей, в котором хранится информация о каждом из отелей
    """

    result = []

    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": dest_id,
                   "pageNumber": "1",
                   "pageSize": "25",
                   "checkIn": "2020-01-08",
                   "checkOut": "2020-01-15",
                   "adults1": "1",
                   "sortOrder": "PRICE_HIGHEST_FIRST",
                   "locale": "en_US",
                   "currency": "USD"
                   }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)

    for i in range(number_of_hotels):
        new_data = {}

        hotel_id = data["data"]["body"]["searchResults"]["results"][i]["id"]
        hotel_name = data["data"]["body"]["searchResults"]["results"][i]["name"]
        address = data["data"]["body"]["searchResults"]["results"][i]["address"]["streetAddress"]
        distance_to_center = data["data"]["body"]["searchResults"]["results"][i]["landmarks"][0]["distance"]
        price = data["data"]["body"]["searchResults"]["results"][i]["ratePlan"]["price"]["current"]
        hotel_photos = get_urls_of_photos(hotel_id, number_of_photos)

        new_data['hotel_name'] = hotel_name
        new_data['address'] = address
        new_data['distance_to_center'] = distance_to_center
        new_data['price'] = price
        new_data['hotel_photos'] = hotel_photos

        result.append(new_data)

    return result


def main(city_name: str,
         number_of_hotels: int,
         need_to_return_photos: bool,
         number_of_photos: int) -> List[Dict[str, str]]:
    destination_id = get_destination_id(city_name)
    if need_to_return_photos:
        return get_all_info(destination_id, number_of_hotels, number_of_photos)
    else:
        return get_all_info(destination_id, number_of_hotels)
