import requests
import json

from api.api_work import search


# list_regId = ['2621', '129440', '41080', '15838', '19768', '4933194', '6203489', '6234083', '2896', '4278092']


def list_properties(city: str, resultsSize: int, check_in_date: str, check_out_date: str):
    list_regId = search(city=city)
    print('list_regId: ', list_regId)
    hotel_dic = dict()

    check_in_day = int(check_in_date.split('.')[0])
    check_in_month = int(check_in_date.split('.')[1])
    check_in_year = int(check_in_date.split('.')[2])

    check_out_day = int(check_out_date.split('.')[0])
    check_out_month = int(check_out_date.split('.')[1])
    check_out_year = int(check_out_date.split('.')[2])

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    try:
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "destination": {"regionId": list_regId[0]},
            # Тут беру первый элемент. Для чего нужны остальные, пока не разобрался
            "checkInDate": {
                "day": check_in_day,
                "month": check_in_month,
                "year": check_in_year
            },
            "checkOutDate": {
                "day": check_out_day,
                "month": check_out_month,
                "year": check_out_year
            },
            "rooms": [
                {
                    "adults": 2,
                    "children": []
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": resultsSize,
            "sort": "PRICE_LOW_TO_HIGH",
            "filters": {"price": {
                "max": 1000,
                "min": 100
            }}
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "6d0cf415c9mshbde68d4de177979p1d2e4bjsnc02c119b3d4a",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        data = json.loads(response.text)

        # запись в словарь hotel_dic отелей попадающих под параметры запроса
        for i in data['data']['propertySearch']['propertySearchListings']:
            if i.get('name') is not None:
                print(i.get('name'))
                propertyImage = i.get('propertyImage')
                url_photo = propertyImage['image']['url']
                print(url_photo)
                # hotel_dic[i.get('name')] = url_photo
                hotel_dic[i.get('name')] = {'id': i.get('id'), 'url_photo': url_photo}

    except Exception as exs:
        print('Ошибка в запросе по городам', exs)

    return hotel_dic, list_regId[0]
