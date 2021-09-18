import logging
import time
from typing import Union

from pyautogui import ImageNotFoundException
from pymsgbox import alert

from config import SANDWICH_FIELD, HIKE_START_FIELD, PROMOTION_NO_TOADSTOOL
from constants import (MAX_FIELD, img_common_return_to_game, img_field_check, img_field_left_arrow, img_field_logo,
                       img_field_popup_no_space_go_home, img_field_popup_no_space_label, img_field_right_arrow,
                       img_hike_go_home, img_main_hike_finish, img_main_hike_finish_ok,
                       img_main_hike_popup_remove_def_ok, img_main_hike_popup_remove_def_title, img_main_in_hike,
                       img_main_in_hike_force, img_main_in_hike_force_apply, img_main_minus, img_main_products_ready,
                       img_common_mushrooms_stolen, img_common_mushrooms_stolen_ok, img_field_antidote,
                       img_field_container)
from helpers.common import get_files_in_dir
from helpers.images import (click_all_by_image, is_image_present, wait_and_click_by_image,
                            wait_and_click_by_image_ignoring_errors, wait_for_image)
from pages.field_page import click_on_next_field_arrow, click_on_return_to_home, get_opened_field, pick_up_my_mushrooms

logger = logging.getLogger(__name__)


class Status:
    OK = "OK"
    OK_MAX_FIELD = "OK. Picking up is finished with max field"
    OK_SANDWICH = "OK. Hike with a lot of fields and need to eat sandwich after it"
    OK_NO_POTION = "no potion to continue a hike"
    OK_SKIPPED_FIELDS = "some fields were skipped in a hike"
    OK_NOTHING_TO_PICK_UP = "no available fields to pick them up"
    NO_SPACE = "no space in the basket"
    NO_HIKE = "Hike is not available yet"


def click_on_in_hike_button(force_hike=False):
    if not wait_and_click_by_image_ignoring_errors(img_main_in_hike):
        if force_hike:
            wait_and_click_by_image(img_main_in_hike_force)
            wait_and_click_by_image(img_main_in_hike_force_apply)
            wait_and_click_by_image(img_main_in_hike)
        else:
            raise ImageNotFoundException("Hike is not available")

    time.sleep(1)
    if is_image_present(img_main_hike_popup_remove_def_title):
        wait_and_click_by_image(img_main_hike_popup_remove_def_ok)
    wait_for_image(img_hike_go_home)


def activate_game():
    status = {"mushrooms_stolen": False}
    # Check if mushrooms were stolen
    if wait_and_click_by_image_ignoring_errors(img_common_mushrooms_stolen):
        wait_and_click_by_image(img_common_mushrooms_stolen_ok)
        status["mushrooms_stolen"] = True

    # any action in game
    wait_and_click_by_image(img_main_minus, confidence=0.8)

    # Click on Return to game button if needed
    if wait_and_click_by_image_ignoring_errors(img_common_return_to_game):
        time.sleep(5)
        # Check if mushrooms were stolen
        if wait_and_click_by_image_ignoring_errors(img_common_mushrooms_stolen):
            wait_and_click_by_image(img_common_mushrooms_stolen_ok)
    return status


def set_minimum_scale():
    wait_and_click_by_image(img_main_minus, confidence=0.8, count=7)


def game_preparation():
    # time.sleep(5)
    status = activate_game()
    set_minimum_scale()
    return status


def get_first_active_field(start_field=1) -> Union[int, None]:
    """
    Get first field on main screen that is ready to picking up.
    """
    for i in range(start_field, MAX_FIELD + 1):
        field = str(i).zfill(2)
        if is_image_present(img_field_logo.format(field)):
            return i


def get_last_active_field(start_field=MAX_FIELD) -> int:
    """
    Get last field on main screen that is ready to picking up.
    """
    for i in range(start_field, 0, -1):
        field = str(i).zfill(2)
        if is_image_present(img_field_logo.format(field)):
            return i
    raise ImageNotFoundException("Active field is not found!")


def launch_mushroom_collection(field: int):
    field = str(field).zfill(2)
    wait_and_click_by_image(img_field_logo.format(field))
    wait_for_image(img_field_check.format(field))


def is_antidote_activated():
    """
    Returns True if antidote is activated or there is promotion that toadstool has no effect.
    """
    if PROMOTION_NO_TOADSTOOL:
        status = True
    else:
        status = is_image_present(img_field_antidote)
    return status


def is_container_activated():
    """
    Returns True if container is activated.
    """
    return is_image_present(img_field_container)


def pick_up_all_mushrooms(is_hike=False, max_field=None, potion=False, antidote=False):
    """
    Picking up all fields.
    Returns status and collected fields count.
    """

    set_minimum_scale()
    field = get_first_active_field()
    start_field = HIKE_START_FIELD if is_hike else 1
    skipped_fields = False
    collected_fields = 0
    if field and start_field > field:
        field = get_first_active_field(start_field)
        skipped_fields = True
    if not field:
        return {"status": Status.OK_NOTHING_TO_PICK_UP, "fields": collected_fields}
    go_to_the_end = bool(SANDWICH_FIELD and get_first_active_field(SANDWICH_FIELD))
    if go_to_the_end:
        max_field = None

    launch_mushroom_collection(field)

    while True:
        collected_fields += pick_up_my_mushrooms(field, potion=potion, antidote=antidote)

        # No space popup
        if is_image_present(img_field_popup_no_space_label):
            wait_and_click_by_image(img_field_popup_no_space_go_home)
            return {"status": Status.NO_SPACE, "fields": collected_fields}

        # Continue playing is right arrow is present. Otherwise, return to home if needed
        if is_image_present(img_field_right_arrow):
            # Go home if field reaches max_field, otherwise continue
            if max_field and field >= max_field:
                click_on_return_to_home()
                return {"status": Status.OK_MAX_FIELD, "fields": collected_fields}
            else:
                click_on_next_field_arrow()
                if is_hike:
                    field = get_opened_field(field + 1)
                else:
                    field += 1
        else:
            if is_hike:
                if skipped_fields:
                    click_on_return_to_home()
                    return {"status": Status.OK_SKIPPED_FIELDS, "fields": collected_fields}
            else:
                click_on_return_to_home()
            break

    return {"status": Status.OK_SANDWICH if go_to_the_end else Status.OK, "fields": collected_fields}


def pick_up_products():
    logger.info("Start picking up products")
    icons = get_files_in_dir(img_main_products_ready)
    for icon in icons:
        click_all_by_image(icon)


def hiking(max_field=None, potion=False, antidote=False):
    result = pick_up_all_mushrooms(is_hike=True, max_field=max_field, potion=potion, antidote=antidote)

    if result["status"] in (Status.OK_MAX_FIELD, Status.OK_NOTHING_TO_PICK_UP, Status.OK_SKIPPED_FIELDS):
        wait_and_click_by_image(img_hike_go_home)

    if result["status"] in (Status.OK, Status.OK_SANDWICH, Status.OK_MAX_FIELD, Status.OK_SKIPPED_FIELDS):
        wait_for_image(img_main_hike_finish)
        wait_and_click_by_image(img_main_hike_finish_ok)

    return result


def go_hike(max_field=None, potion=False, force_hike=False, antidote=False):
    try:
        click_on_in_hike_button(force_hike)
    except ImageNotFoundException:
        logger.info("Hike is not available")
        return {"status": Status.NO_HIKE, "fields": 0}

    return hiking(max_field, potion, antidote)


def go_hike_mail():
    pass


def is_hike_available():
    if is_image_present(img_main_in_hike):
        logger.info("Hike is available!")
        return True
    else:
        logger.info("Hike is not available!")
        return False


def wait_for_hike_is_available():
    logger.info("Wait for hike is available")
    while True:
        activate_game()
        if is_hike_available():
            break
        time.sleep(30)

