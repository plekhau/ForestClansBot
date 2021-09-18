from time import sleep

from pyautogui import ImageNotFoundException

from constants import (MAIL_PAGES_AMOUNT, img_hike_go_home, img_mail_arrow_left, img_mail_arrow_right, img_mail_close,
                       img_mail_go_hike, img_mail_hikes_to_you_tab_disabled, img_main_mail,
                       img_main_hike_popup_remove_def_ok)
from helpers.images import (click, get_all_coordinates_by_image, is_image_present_wait, wait_and_click_by_image,
                            wait_and_click_by_image_ignoring_errors, wait_for_image, wait_for_no_image)
from pages.main_page import hiking


def open_mails():
    """
    Opens Mails
    """
    wait_and_click_by_image(img_main_mail)
    wait_for_image(img_mail_close)


def close_mails():
    """
    Closes Mails
    """
    wait_and_click_by_image(img_mail_close)
    wait_for_no_image(img_mail_close)


def next_page(count=1):
    """
    Click on right arrow 'count' times
    """
    wait_and_click_by_image(img_mail_arrow_right, count=count)
    sleep(0.5)


def previous_page(count=1):
    """
    Click on left arrow 'count' times
    """
    wait_and_click_by_image(img_mail_arrow_left, count=count)
    sleep(0.5)


def open_last_page():
    try:
        next_page(MAIL_PAGES_AMOUNT - 1)
    except ImageNotFoundException:
        # Arrow can be not visible if not the first page was opened
        pass


def open_hikes_to_you_tab():
    wait_and_click_by_image_ignoring_errors(img_mail_hikes_to_you_tab_disabled)


def go_hike_from_mails(max_field=None, potion=False, antidote=False):
    is_hike_possible = False

    # Open Mails popup
    open_mails()

    # Open the last page
    open_last_page()

    # Go through all pages
    for i in range(MAIL_PAGES_AMOUNT):
        # Find available hikes on current page
        hikes = get_all_coordinates_by_image(img_mail_go_hike)
        print(f"Hikes: {hikes}")
        for hike in hikes:
            # Try to click on Go Hike button
            click(*hike)

            # Check if hike started
            sleep(0.5)
            wait_and_click_by_image_ignoring_errors(img_main_hike_popup_remove_def_ok)
            if is_image_present_wait(img_hike_go_home):
                return hiking(max_field, potion, antidote)
            else:
                is_hike_possible = True

        # Go to previous page
        if i < MAIL_PAGES_AMOUNT - 1:
            previous_page()

    # Close Mails popup
    close_mails()

    return is_hike_possible


# go_hike_from_mails(antidote=True)
# hiking(antidote=True)
