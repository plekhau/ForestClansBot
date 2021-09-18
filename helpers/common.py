import logging
import os
import subprocess
import time
import traceback
from os import listdir
from os.path import isfile, join

import pyautogui
from pymsgbox import alert

from config import MY_MAX_FIELD
from constants import PATH_TO_APP, img_common_return_to_game
from helpers.images import get_screenshot, wait_and_click_by_image_ignoring_errors

logger = logging.getLogger(__name__)


def get_hike_delay(fields):
    """
    Time in seconds that need to wait before next hike after picking up of 'fields' fields
    """
    return 7 * 60 + fields * 90


def get_my_max_collecting_time():
    """
    Returns approximate time in second that needs to collecting all my fields
    """
    return 30 * MY_MAX_FIELD


def repeat(times=3):
    """
    Repeats function until it passes.
    Fails if it failed after 'times' attempts.
    """

    def decorator(function):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    return function(*args, **kwargs)
                except Exception as e:
                    logger.info("Attempt failed")
                    logger.debug(traceback.print_exc())
                    logger.debug(str(e))
                    time.sleep(1)
            raise AssertionError("{}: all {} attempts failed".format(function.__name__, times))

        return wrapper

    return decorator


def repeat_if_return_to_game_error(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                result = func(*args, **kwargs)
                break
            except Exception as ex:
                if not wait_and_click_by_image_ignoring_errors(img_common_return_to_game):
                    raise ex
                logger.warning(f"Restart function: {func}")
        return result
    return wrapper


def get_files_in_dir(path):
    """
    Returns list of files in directory
    """
    return [join(path, f) for f in listdir(path) if isfile(join(path, f))]


def countdown(minutes: int):
    while minutes > 0:
        logger.info(f"Minutes left: {minutes}")
        time.sleep(60)
        minutes -= 1


def start_app():
    """
    Launch Forest & Clans game
    """
    logger.info("Launch Forest & Clans game")
    subprocess.Popen([PATH_TO_APP])
    time.sleep(10)
    pyautogui.keyDown('winleft')
    pyautogui.press('up')
    pyautogui.keyUp('winleft')


def stop_app():
    """
    Close Forest & Clans game
    """
    logger.info("Close Forest & Clans game")
    os.system("taskkill /im ForestClans.exe")


def restart_app(timeout: int):
    """
    Restart Forest & Clans game

    Usage: close game to invite somebody in hike to us
    """
    stop_app()
    countdown(timeout)
    start_app()


def teardown():
    """
    Save current screenshot if script finishes unexpectedly.
    """
    time_str = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
    get_screenshot().save(f"teardown_{time_str}.png")
    alert(text="Script finished unexpectedly", title="Forest Clans", button="OK")
