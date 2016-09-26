import json
import math
from geopy.distance import great_circle


def load_data(filepath):
    """Декодирует json-данные в Python-объект. Возвращает список,
    элементами которого являются словари(dicts), предоставляющие 
    информацию о барах Москвы."""

    with open(filepath) as f:
        bars_json = f.readline()
        bars_data = json.loads(bars_json)
    return bars_data


def get_biggest_bar(data):
    """Находит бар с наибольшим количеством посадочных мест.
    Возвращает название этого бара."""

    biggest_bar = max(data, key=lambda x: x['Cells']['SeatsCount'])
    name = biggest_bar['Cells']['Name']
    return name


def get_smallest_bar(data):
    """Находит бар с наименьшим количеством посадочных мест.
    Возвращает название этого бара."""

    smallest_bar = min(data, key=lambda x: x['Cells']['SeatsCount'])
    name = smallest_bar['Cells']['Name']
    return name


def get_closest_bar(data, longitude, latitude):
    """Находит ближайший бар на основании координат, введённых пользователем 
    с клавиатуры. 
    longitude -- долгота
    latitude -- широта

    Расстояние от пользователя до ближайшего бара вычисляется с помощью
    функции grea_circle из модуля geopy"""
    
    my_location = (latitude, longitude)
    min_distance = 21*10**6
    for bar in data:
        bar_location = bar['Cells']['geoData']['coordinates']
        distance = great_circle(my_location, bar_location).meters
        if distance < min_distance:
            min_distance = distance
            name = bar['Cells']['Name']
    return name


if __name__ == '__main__':
    filepath = input("Введите путь к файлу json --- ")
    try:
        bars_data = load_data(filepath)
    except FileNotFoundError:
        print("Нет такого файла или директории! Повторите ввод.")
        exit()
    longitude, latitude = [float(coord) for coord in 
                           input("Через пробел введите текущие GPS-координаты --- ").split()]

    smallest_bar_name = get_smallest_bar(bars_data)
    biggest_bar_name = get_biggest_bar(bars_data)
    closest_bar_name = get_closest_bar(bars_data, longitude, latitude)

    print("\nСамый большой бар в Москве -- \"%s\"" % biggest_bar_name)
    print("Самый маленький бар в Москве -- \"%s\"" % smallest_bar_name)
    print("Ближайший бар -- \"%s\"" % closest_bar_name)
