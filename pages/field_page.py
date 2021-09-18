import logging
import random
import time
from typing import Union

from pyautogui import ImageNotFoundException

from config import FIELD_ATTEMPTS, ALLOWED_POTIONS
from constants import (DEFAULT_FIELD_ATTEMPTS, MAX_FIELD, img_field_check, img_field_finish, img_field_finish_ok,
                       img_field_hide_folder, img_field_mushroom_rain, img_field_return_to_home, img_field_right_arrow,
                       img_field_star, img_field_potions, Potions, LUCK_POTION_ATTEMPTS, ENERGY_POTION_ATTEMPTS,
                       TOADSTOOL_ATTEMPTS)
from helpers.common import get_files_in_dir
from helpers.images import (click_all_by_image, is_image_present, wait_and_click_by_image, wait_and_click_on_any_image,
                            wait_for_no_image, get_all_coordinates_by_image, wait_and_click_by_image_ignoring_errors)

logger = logging.getLogger(__name__)


def click_on_ok_button_on_finish_popup():
    wait_and_click_by_image(img_field_finish_ok, timeout=10)
    time.sleep(1)


def click_on_next_field_arrow():
    wait_and_click_by_image(img_field_right_arrow)
    time.sleep(1)


def click_on_return_to_home():
    wait_and_click_by_image(img_field_return_to_home)
    time.sleep(1)


def get_stars() -> int:
    """
    Returns current progress of picking up (0-3 stars)
    """
    stars = len(get_all_coordinates_by_image(img_field_star))
    logger.info(f"Stars: {stars}")
    return stars


def apply_potion() -> Union[Potions, None]:
    """
    Applies potion according to 'ALLOWED_POTIONS' and returns applied potion.
    Returns None if none of potions were applied.
    """
    for potion in ALLOWED_POTIONS:
        if wait_and_click_by_image_ignoring_errors(img_field_potions + potion):
            logger.info(f"Potion: {potion}")
            return potion
    logger.info("No potions are available!")


def get_opened_field(start_field=1, reverse=False) -> int:
    """
    Get number of current opened field or None if field is unknown. Check starts from 'start_field'.
    start_field - the first field to check
    reverse - defines the order of the check

    Usage:
        Need to check field number because when field is changed using arrows some of field can be skipped in hike.
    """
    if reverse:
        last_field = 0
        step = -1
    else:
        last_field = MAX_FIELD + 1
        step = 1

    for field in range(start_field, last_field, step):
        field_str = str(field).zfill(2)
        if is_image_present(img_field_check.format(field_str)):
            logger.info(f"Current field is {field}")
            return field

    raise ImageNotFoundException("Current field is unknown!")


def fast_pick_up_mushrooms(field: int, limit: int):
    """
    Fast picking up without additional checks that it's done + using one screenshot to speed up
    Picks up no more than 'limit' mushrooms
    """
    logger.info(f"Fast picking up: {limit} mushrooms")
    field = str(field).zfill(2)
    hide_files = get_files_in_dir(img_field_hide_folder.format(field))
    random.shuffle(hide_files)
    while limit > 0:
        found = False
        for hide in hide_files:
            clicked = click_all_by_image(hide, limit=limit)
            limit -= clicked
            if limit == 0:
                break
            if clicked > 0:
                found = True
        if not found:
            # Exit if none of mushrooms were picked up during iteration
            break


def pick_up_my_mushrooms(field: int, potion=False, antidote=False):
    """
    Picking up mushrooms for one field.
    Returns 0 if there is nothing to pick up, otherwise returns 1.
    """
    print(f"Pick up field: {field}")
    try:
        wait_for_no_image(img_field_mushroom_rain, exception=False)
    except ImageNotFoundException:
        return 0

    # Activate Harvest potion before picking up if needed
    if potion:
        if Potions.HARVEST in ALLOWED_POTIONS:
            if wait_and_click_by_image_ignoring_errors(img_field_potions + Potions.HARVEST):
                logger.info(f"Potion: {potion}")

    # Limit: attempts per field
    # minus 1 (to stop before the last mushroom to use portion)
    # minus 3 (toadstool) if there is no antidote
    limit = FIELD_ATTEMPTS.get(field, DEFAULT_FIELD_ATTEMPTS) - (1 if potion else 0) - (0 if antidote else TOADSTOOL_ATTEMPTS)
    fast_pick_up_mushrooms(field, limit)

    is_absolut_used = False
    if potion:
        stars = get_stars()
        if stars == 0:
            applied_potion = apply_potion()
            if applied_potion == Potions.LUCK:
                additional_attempts = LUCK_POTION_ATTEMPTS - FIELD_ATTEMPTS.get(field, DEFAULT_FIELD_ATTEMPTS)
                fast_pick_up_mushrooms(field, additional_attempts)
            elif applied_potion == Potions.ENERGY:
                fast_pick_up_mushrooms(field, ENERGY_POTION_ATTEMPTS)
            elif applied_potion == Potions.ABSOLUT:
                is_absolut_used = True


    field = str(field).zfill(2)
    hide_files = get_files_in_dir(img_field_hide_folder.format(field))
    while not is_absolut_used and not is_image_present(img_field_finish):
        random.shuffle(hide_files)
        try:
            wait_and_click_on_any_image(hide_files)
        except ImageNotFoundException as ex:
            if not is_image_present(img_field_finish):
                raise ex

    click_on_ok_button_on_finish_popup()
    return 1
