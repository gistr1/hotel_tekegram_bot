import time
from telebot import types

import commands
from api.endpoint_list import list_properties
from api.get_offers import get_hotel_offers
from api.get_photo import hotel_photo
from calenar import select_from_calenar_check_in, MyState, user_dates
from commands.start import get_start

from database.database import logging
from main import bot
import re

from telebot.handler_backends import State, StatesGroup  # States

user_req = dict()
user_response = dict()
sticer_id = 'CAACAgIAAxkBAAEG8PpjpCz9oGtfQoPyYSYH_bQhlR_a-gACIwADKA9qFCdRJeeMIKQGLAQ'


@bot.message_handler(commands=['lowprice'])
@logging
def get_lowprice(foo_message):
    msg = bot.send_message(foo_message.from_user.id, "Команда /lowprice. Введи город на латинице")
    bot.set_state(foo_message.from_user.id, MyState.city, foo_message.from_user.id)


@bot.message_handler(state=MyState.city)
def get_city(foo_message):
    print('выполняется get city')
    city = foo_message.text
    user_req[foo_message.from_user.id] = {'city': city}
    print('Буду искать в городе', city)

    bot.set_state(foo_message.from_user.id, MyState.check_in, foo_message.from_user.id)
    select_from_calenar_check_in(foo_message)


@bot.message_handler(state=MyState.count_hotel)
def get_resultsSize(foo_message):
    print('Исходный словарь', user_req)
    user_req[foo_message.from_user.id].update(user_dates[foo_message.from_user.id])
    print('обновил словарь', user_req)

    try:
        resultsSize = int(foo_message.text)
        user_req[foo_message.from_user.id].update({'resultsSize': resultsSize})
        print('Буду искать {} отелей'.format(resultsSize))

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_yes = types.KeyboardButton('Да')
        item_no = types.KeyboardButton('Нет')
        keyboard.add(item_yes, item_no)

        bot.send_message(foo_message.from_user.id, text='Выводим фотки отеля? (Да/Нет)', reply_markup=keyboard)

        bot.register_next_step_handler(foo_message, print_photo)


    except ValueError:
        bot.send_message(foo_message.from_user.id, "Проблема с количеством отелей, необходимо ввести целое число? ")
        bot.register_next_step_handler(foo_message, get_resultsSize)


def print_photo(foo_message):
    if foo_message.text.lower() == 'да':
        bot.send_message(foo_message.from_user.id, "Введи кол-во фоток ")
        bot.register_next_step_handler(foo_message, get_hotel_photo)

    elif foo_message.text.lower() == 'нет':
        make_request(foo_message, flag=False)


def get_hotel_photo(foo_message):  # Если надо выводить фотки, то мы вызываем функцию make_request с флагом True
    cont_photo = foo_message.text
    if cont_photo.isdigit():
        cont_photo = int(cont_photo)
        make_request(foo_message, flag=True, count=cont_photo)


    else:
        bot.send_message(foo_message.from_user.id, "Проблема с вводом. Введи целое число")
        bot.register_next_step_handler(foo_message, get_hotel_photo)


def checkdate(date: str) -> bool:
    """
Функция, которая проверяет дату на формат dd.mm.yyyy
    :param date: str
    :return: bool
    """
    try:
        time.strptime(date, '%d.%m.%Y')
        print('Date ok')
        return True
    except ValueError:
        print('Invalid date!')
        return False


def make_request(foo_message, flag, count=0):
    print(user_req)
    msg = foo_message

    city = user_req[foo_message.from_user.id]['city']
    resultsSize = user_req[foo_message.from_user.id]['resultsSize']
    checkindate = user_req[foo_message.from_user.id]['checkindate']
    checkoutdate = user_req[foo_message.from_user.id]['checkoutdate']

    print('Дата заезда: ', checkindate)
    print('Дата выезда', checkoutdate)
    print('Делаю запрос по городу', city)
    bot.send_sticker(foo_message.from_user.id, sticer_id)
    hotels, region_id = list_properties(city=city, resultsSize=resultsSize, check_in_date=checkindate,
                                        check_out_date=checkoutdate)
    print('Найденные отели: ', hotels)

    check_in_day = int(checkindate.split('.')[0])
    check_in_month = int(checkindate.split('.')[1])
    check_in_year = int(checkindate.split('.')[2])

    check_out_day = int(checkoutdate.split('.')[0])
    check_out_month = int(checkoutdate.split('.')[1])
    check_out_year = int(checkoutdate.split('.')[2])

    if len(hotels) > 0:

        user_response[msg.from_user.id] = {}
        for name_hotel, data in hotels.items():
            # bot.send_message(foo_message.from_user.id, name_hotel)
            hotel_id = data.get('id')
            url = data.get('url_photo')

            print('name', name_hotel)
            print('id', hotel_id)
            print('Фото', url)

            photos, hotel_latitude, hotel_longitude, hotel_reviews_rating, hotel_address_line = hotel_photo(hotel_id)
            price_message = get_hotel_offers(property_id=hotel_id, in_day=check_in_day, in_month=check_in_month,
                                             in_year=check_in_year, out_day=check_out_day, out_month=check_out_month,
                                             out_year=check_out_year, latitude=hotel_latitude,
                                             longitude=hotel_longitude, region_id=region_id)

            user_response[msg.from_user.id][hotel_id] = {'data': [], 'photo': []}
            # собираем инфу по отелю в словарь
            user_response[msg.from_user.id][hotel_id]['data'].append(
                'Название отеля: {name}\nАдрес отеля: {adress}\nРейтинг отеля: {id}\nСтоимость отеля: {price}\n'.format(
                    name=name_hotel, adress=hotel_address_line, id=hotel_reviews_rating,
                    price=price_message))

            if flag is True:

                for index, url_photo in enumerate(iter(photos)):
                    if index < count:
                        # bot.send_photo(msg.from_user.id, url_photo)
                        user_response[msg.from_user.id][hotel_id]['photo'].append(url_photo)

                    else:
                        break

        for i_hotel in user_response[msg.from_user.id]:
            bot.send_message(msg.from_user.id, user_response[msg.from_user.id][f'{i_hotel}']['data'])
            if flag is True:
                for i_url_photo in user_response[msg.from_user.id][f'{i_hotel}']['photo']:
                    bot.send_photo(msg.from_user.id, i_url_photo)

    else:
        bot.send_message(foo_message.from_user.id, 'Ничего не найдено /start')

    print(user_req)
    get_start(foo_message)
