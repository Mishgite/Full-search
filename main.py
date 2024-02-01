import sys
import requests
import os
import pygame
from map_scale_utils import get_scale_params


def show_map(object_longitude, object_latitude):
    map_params = get_scale_params(object_longitude, object_latitude)
    map_params["l"] = "map"

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    os.remove(map_file)


def get_object_coordinates(toponym):
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_latitude = toponym_coodrinates.split(" ")
    return toponym_longitude, toponym_latitude


def main():
    toponym_to_find = " ".join(sys.argv[1:])
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print("Ошибка выполнения запроса")
        return

    toponym = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    object_longitude, object_latitude = get_object_coordinates(toponym)
    show_map(float(object_longitude), float(object_latitude))


if __name__ == "__main__":
    main()
