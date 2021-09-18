import random

from pyautogui import Point

from config import PRODUCT_AMOUNT
from constants import (img_house_production_logos, img_house_production_menu_cook, img_house_production_popup_close,
                       img_house_production_popup_left_conner, img_house_production_popup_right_arrow,
                       img_house_production_popup_right_conner)
from helpers.common import get_files_in_dir, repeat
from helpers.images import click, get_coordinates_by_image, wait_and_click_by_image, wait_for_image

DRIER_FIELDS = [1, 2, 3, 4, 6, 8, 11, 13, 14, 21, 25]
BARREL_FIELDS = [1, 2, 3, 5, 7, 9, 12, 15, 18, 24, 29]
POT_FIELDS = [2, 3, 4, 5, 7, 9, 12, 15, 17, 19, 22, 37]
STOVE_FIELDS = [1, 4, 6, 8, 10, 13, 16, 18, 20, 23, 26, 36]
FRIDGE_FIELDS = [5, 6, 9, 10, 11, 14, 16, 17, 20, 24, 28]
CONVEYOR_FIELDS = [7, 10, 11, 15, 19, 22, 23, 27, 28, 30, 35]
PIZZA_FIELDS = [8, 13, 14, 16, 21, 25, 26, 27, 29, 32, 33]
BRAZIER_FIELDS = [18, 21, 23, 25, 27, 28, 29, 30, 31, 32, 34, 38]


class Productions:
    DRIER = "Drier"  # Сушилка
    BARREL = "Barrel"  # Бочка
    POT = "Pot"  # Чан
    STOVE = "Stove"  # Печь
    FRIDGE = "Fridge"  # Холодильник
    CONVEYOR = "Conveyor"  # Конвеер
    PIZZA = "Pizza"  # Печь для пиццы
    BRAZIER = "Brazier"  # Мангал
    WOK = "Wok"  # Вок


def calculate_product_coordinates():
    left_conner = get_coordinates_by_image(img_house_production_popup_left_conner, point="top-right")
    right_conner = get_coordinates_by_image(img_house_production_popup_right_conner, point="top-left")
    size = (right_conner.x - left_conner.x) // 6
    start_point = Point(right_conner.x - size // 2, right_conner.y - size // 2)
    points = [Point(start_point.x - x * size, start_point.y - y * size) for y in range(2) for x in range(6)]
    points.reverse()
    print(points)
    return points


@repeat(times=10)
def open_production():
    """
    Opens random production
    """
    icons = get_files_in_dir(img_house_production_logos)
    product_to_open = random.choice(icons)
    wait_and_click_by_image(product_to_open)
    wait_and_click_by_image(img_house_production_menu_cook)
    wait_for_image(img_house_production_popup_close)


def close_production():
    wait_and_click_by_image(img_house_production_popup_close)


def cook_all_productions():
    open_production()
    product_coordinates = calculate_product_coordinates()
    next_button_coordinates = get_coordinates_by_image(img_house_production_popup_right_arrow)
    for _ in range(PRODUCT_AMOUNT-1):
        for point in product_coordinates:
            click(*point)
        click(*next_button_coordinates)
    close_production()
