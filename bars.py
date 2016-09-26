import json
import math


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

    Основываясь на формуле "Spherical law of cosines" для нахождения расстояния
    между двумя точками на земном шаре, взятой из статьи 
    https://en.wikipedia.org/wiki/Great-circle_distance ,
    производится поиск ближайшего бара. 

    Возвращает название бара"""

    earth_radius = 6372795
    latitude, longitude = math.radians(latitude), math.radians(longitude)
    sin_lat, cos_lat = math.sin(latitude), math.cos(latitude)
    min_distance = 21*10**6
    for bar in data:
        bar_lat, bar_longit = bar['Cells']['geoData']['coordinates']
        bar_lat, bar_longit = math.radians(bar_lat), math.radians(bar_longit)
        sin_bar_lat, cos_bar_lat = math.sin(bar_lat), math.cos(bar_lat)
        cos_delta_longit = math.cos(bar_longit - longitude)
        central_angle = math.acos(sin_lat*sin_bar_lat+
                                  cos_lat*cos_bar_lat*cos_delta_longit)
        distance = earth_radius*central_angle
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

    print("\nСамый большой бар в Москве - \"%s\"" % biggest_bar_name)
    print("Самый маленький бар в Москве - \"%s\"" % smallest_bar_name)
    print("Ближайший бар - \"%s\"" % closest_bar_name)
