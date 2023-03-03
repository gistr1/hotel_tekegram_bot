from typing import Type

import requests
import json


def search_destination(dest: str) -> str:
    """
Функция которая делает запрос в locations/v3/search по местоположению dest и возвращает текст ответа (JSON)
    :param dest: str
    :return: str
    """

    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    print('Делаю запрос по городу {town} на {url}'.format(town=dest, url=url))
    querystring = {"q": dest, "locale": "en_US", "langid": "1033", "siteid": "300000001"}

    headers = {
        "X-RapidAPI-Key": "6d0cf415c9mshbde68d4de177979p1d2e4bjsnc02c119b3d4a",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.text


def import_destination_id(json_text: str) -> list:
    """
Функция, которая  вытягивает поля 'gaiaId' 'hotelId' из ответа на запрос locations/v3/search
    :param json_text: str
    :return: list(int)
    """
    try:
        data = json.loads(json_text)
        destination_id = [sr.get('gaiaId') or sr.get('hotelId') for sr in data['sr']]
        return destination_id
    except Exception as exc:
        print('Ошибка в импорте json ', exc)
        destination_id = []
        return destination_id


def search(city):
    result = search_destination(city)
    regionId = import_destination_id(result)

    return regionId
