from constants import (img_house_laboratory_logo, img_house_laboratory_menu_create_potion,
                       img_house_laboratory_popup_close, img_house_laboratory_popup_potions,
                       img_house_laboratory_popup_title)
from helpers.common import repeat
from helpers.images import wait_and_click_by_image, wait_for_image, wait_for_no_image


@repeat()
def open_laboratory():
    """
    Opens Laboratory
    """
    wait_and_click_by_image(img_house_laboratory_logo)
    wait_and_click_by_image(img_house_laboratory_menu_create_potion)
    wait_for_image(img_house_laboratory_popup_title)


def close_laboratory():
    """
    Closes Laboratory
    """
    wait_and_click_by_image(img_house_laboratory_popup_close)
    wait_for_no_image(img_house_laboratory_popup_title)


def choose_potions(potions: dict):
    """
    Chooses potions.

    :param potions: dict in format <Potion: count>
    """
    for potion, count in potions.items():
        wait_and_click_by_image(img_house_laboratory_popup_potions + potion, count=count)


def create_potions(potions: dict):
    open_laboratory()
    choose_potions(potions)
    close_laboratory()
