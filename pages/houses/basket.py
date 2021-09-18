import logging

from pyautogui import ImageNotFoundException

from config import FIELDS_NOT_FOR_SALE, NO_SALE
from constants import img_house_basket_logo, img_house_basket_menu_mushrooms, img_house_basket_popup_title, \
    img_house_basket_mushroom, img_house_basket_popup_sell, MAX_FIELD, img_house_basket_popup_empty_basket, \
    img_house_basket_popup_close, img_house_basket_popup_empty_slot
from helpers.images import wait_and_click_by_image, wait_for_image, is_image_present, wait_for_no_image, \
    get_all_coordinates_by_image, wait_and_click_by_image_ignoring_errors

logger = logging.getLogger(__name__)

SLOT_COUNT = 15


def get_count_of_empty_slots():
    slot_count = len(get_all_coordinates_by_image(img_house_basket_popup_empty_slot, confidence=0.95))
    logger.info(f"Empty slots: {slot_count}")
    return slot_count


def open_basket():
    wait_and_click_by_image(img_house_basket_logo)
    wait_and_click_by_image(img_house_basket_menu_mushrooms, confidence=0.8)
    # wait_for_image(img_house_basket_popup_title)


def close_basket():
    wait_and_click_by_image(img_house_basket_popup_close)
    wait_for_no_image(img_house_basket_popup_title)


def sell_one_mushroom(field: int):
    field = str(field).zfill(2)
    if wait_and_click_by_image_ignoring_errors(img_house_basket_mushroom.format(field)):
        wait_and_click_by_image(img_house_basket_popup_sell)


def sell_some_mushrooms(save=True):
    # TODO: it works only for MY_MAX_FIELD < 15
    expected_empty_slots = SLOT_COUNT - len(FIELDS_NOT_FOR_SALE)
    for field in range(1, MAX_FIELD + 1):
        if save and field in FIELDS_NOT_FOR_SALE:
            continue
        if not sell_one_mushroom(field) and get_count_of_empty_slots() >= expected_empty_slots:
            # Return if mushroom is not sold and there is nothing to sell
            return


def sell_mushrooms(save=True):
    if NO_SALE:
        # don't sell any mushrooms if NO_SALE setting is True
        return
    open_basket()
    sell_some_mushrooms(save)
    close_basket()

