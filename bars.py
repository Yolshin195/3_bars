# -*- coding: UTF-8 -*-

import json
import sys
import os.path
import math


def load_json_data(filepath):
    if not os.path.exists(filepath) and not filepath.endswith(".json"):
        return None
    with open(filepath, "r") as f:
        return json.load(f)


def get_biggest_bar(data):
    return max(data, key=lambda max_key: max_key['SeatsCount'])


def get_smallest_bar(data):
    return min(data, key=lambda min_key: min_key['SeatsCount'])


def get_closest_bar(data, longitude, latitude):
    return min(data, key=lambda min_key: distBar(
        min_key['Latitude_WGS84'], latitude,
        min_key['Longitude_WGS84'], longitude
    ))


def convertInRadians(coordinate):
    return float(coordinate) * math.pi/180.


def distBar(latitude1, latitude2, Longitude1, longitude2, rad=6372795):
    """
        сверическая теорема косинусов
        pi число pi rad - радиус сферы(Земли)
        dist - растояние между двумя точками
    """
    # кординаты двух точек в радианах
    lat1 = convertInRadians(latitude1)
    lat2 = convertInRadians(latitude2)
    long1 = convertInRadians(Longitude1)
    long2 = convertInRadians(longitude2)

    # косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # вычисление длинны большого круга
    y = math.sqrt(math.pow(cl2*sdelta, 2)) + math.pow(
            cl1 * sl2 - sl1 * cl2 * cdelta, 2
        )
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    dist = ad * rad

    return dist


if __name__ == '__main__':
    data = load_json_data(sys.argv[1])
    dataOutput = None

    print("""
    1 - Самый большой бар
    2 - самый маленький бар
    3 - Ближайший бар по отношения к вам
    """)

    i = input("Ведите число от 1 до 3: ")

    if i == "1":
        dataOutput = get_biggest_bar(data), "Самый большой бар"

    elif i == "2":
        dataOutput = get_smallest_bar(data), "Самый маленький бар"

    elif i == "3":
        dataOutput = get_closest_bar(
            data,
            input("Введите широту: "),
            input("Введите долготу: ")
        ), "Самый ближайший бар"

    else:
        print("Ошибка ввода")

    if dataOutput:
        print("""
    *** {} ***

    Название: {Name}
    Административный округ: {AdmArea}
    Район: {District}
    Адрес: {Address}
    Контактные данные: {PublicPhone[0][PublicPhone]}
    Количество сидячих мест: {SeatsCount}
        """.format(dataOutput[1], **dataOutput[0]))
