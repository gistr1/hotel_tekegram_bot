import functools

import requests
import json
import dpath.util


def hotel_photo(property_id: str):
    try:
        url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
        url_get_summary = "https://hotels4.p.rapidapi.com/reviews/v3/get-summary"

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "propertyId": property_id
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "6d0cf415c9mshbde68d4de177979p1d2e4bjsnc02c119b3d4a",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        response_get_summary = requests.request("POST", url_get_summary, json=payload,
                                                headers=headers)  # для запроса рейтинга

        data = json.loads(response.text)
        data_get_summary = json.loads(response_get_summary.text)

        object_images_hotel = (images for images in data['data']['propertyInfo']['propertyGallery'][
            'images'])  # Получаю объект из 'images' для каждого отеля
        object_url_image_hotel = (url['image']['url'] for url in
                                  object_images_hotel)  # Получаю объект из 'url' для каждого 'images' отеля

        hotel_name = dpath.get(data, 'data/propertyInfo/summary/name')
        print('Имя отеля', hotel_name)

        hotel_address_line = dpath.get(data, 'data/propertyInfo/summary/location/address/addressLine')
        print('Адрес отеля', hotel_address_line)

        hotel_latitude = dpath.get(data, 'data/propertyInfo/summary/location/coordinates/latitude')
        hotel_longitude = dpath.get(data, 'data/propertyInfo/summary/location/coordinates/longitude')
        hotel_reviews_rating = dpath.get(data_get_summary,
                                         'data/propertyReviewSummaries/0/overallScoreWithDescriptionA11y/value')
        print(hotel_latitude)
        print(hotel_longitude)
        print(hotel_reviews_rating)

        return object_url_image_hotel, hotel_latitude, hotel_longitude, hotel_reviews_rating, hotel_address_line

    except Exception as exc:
        print('Ошибка в функции  get_hotel_photo', exc)

# count = 5
# photo_url_hotel = hotel_photo('1784514')
# if photo_url_hotel is not None:
#     print('Фото отелей:')
#     for index, url in enumerate(iter(photo_url_hotel)):
#         if index < count:
#             print('Фото№ ', index)
#             print(url)
#         else:
#             break
# else:
#     print('Информация не найдена')
