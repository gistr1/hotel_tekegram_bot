import requests
import json
import dpath.util


def get_hotel_offers(property_id, in_day, in_month, in_year, out_day, out_month, out_year, latitude, longitude,
                     region_id):
    url = "https://hotels4.p.rapidapi.com/properties/v2/get-offers"
    result_get_offers = dict()
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": "{property_id}".format(property_id=property_id),
        "checkInDate": {
            "day": in_day,
            "month": in_month,
            "year": in_year
        },
        "checkOutDate": {
            "day": out_day,
            "month": out_month,
            "year": out_year
        },
        "destination": {
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "regionId": "{region_id}".format(region_id=region_id)
        },
        "rooms": [
            {
                "adults": 2,
                "children": []
            }

        ]
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "6d0cf415c9mshbde68d4de177979p1d2e4bjsnc02c119b3d4a",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response_offers = requests.request("POST", url, json=payload, headers=headers)

    data = json.loads(response_offers.text)
    print(response_offers)

    hotel_id = dpath.get(data, 'data/propertyOffers/id')
    print('id отеля', hotel_id)
    result_get_offers[hotel_id] = {}

    price_list = [round(total_price[1]) for total_price in
                  dpath.search(data,
                               '**/primarySelections/0/propertyUnit/ratePlans/0/priceDetails/0/price/total/amount',
                               yielded=True)]
    if min(price_list) == max(price_list):
        price_message = '{price}$'.format(price=min(price_list))
    else:
        price_message = f'от {min(price_list)}$ до {max(price_list)}$'
    result_get_offers[hotel_id] = {'price': price_list}

    photo_list = (photo[1] for photo in dpath.search(data, '**/image/url',
                                                     yielded=True))

    result_get_offers[hotel_id].update({'photo': photo_list})
    print(result_get_offers)

    test = dpath.search(data, '**/url', yielded=True)
    print(list(test))
    return price_message
