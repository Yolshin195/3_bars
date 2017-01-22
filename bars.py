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
    return min(data, key=lambda min_key: distBar(min_key['Latitude_WGS84'], latitude, min_key['Longitude_WGS84'], longitude))
     

def distBar( latitude1, latitude2, Longitude1, longitude2, rad=6372795):
    """
        pi число pi rad - радиус сферы(Земли)
        argument: lat1=number, lat2=number, long1=number, long2=number 
    """
    #кординаты двух точек в радианах
    lat1 = float(latitude1) * math.pi/180.
    lat2 = float(latitude2) * math.pi/180.
    long1 = float(Longitude1) * math.pi/180.
    long2 = float(longitude2) * math.pi/180.
    
    #косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    #вычисление длинны большого круга
    y = math.sqrt(math.pow(cl2*sdelta, 2)) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2)
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y,x)
    dist = ad * rad

    return dist

def output(data, text):
    return("""*** {} ***\n Название: {Name} 
    Адресс: {Address}
    """.format(text, **data))


def main(v, data):
    test ={
            "1": [get_biggest_bar(data), "Самый большой бар"],
            "2": [get_smallest_bar(data), "Самый маленький бар"],
            "3": [get_closest_bar(data, input("Ведите долготу: "), input("Введите широту: ")), "Ближе всего квам расположен бар"]
            }
    return output(test[v][0], test[v][1])

if __name__ == '__main__':
    data = load_json_data(sys.argv[1])
    print(main(input(), data))
