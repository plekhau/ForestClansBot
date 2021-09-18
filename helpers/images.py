import logging
import time
from functools import partial
from typing import List

import pyautogui
from PIL import ImageGrab

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

logger = logging.getLogger(__name__)

DEFAULT_CONFIDENCE = 0.9


def click(x, y):
    """
    Click and come back to current coordinates.
    Allows to do something on one monitor if game is playing on another one
    """
    current_coordinates = pyautogui.position()
    pyautogui.click(x, y)
    # pyautogui.moveTo(*current_coordinates)


def _locate_all(path: str, confidence=DEFAULT_CONFIDENCE, distance=10):
    distance = pow(distance, 2)
    elements = []
    for element in pyautogui.locateAllOnScreen(path, confidence=confidence):
        if all(map(lambda x: pow(element.left - x.left, 2) + pow(element.top - x.top, 2) > distance, elements)):
            elements.append(element)
    return elements


def _locate_one(path: str, confidence=DEFAULT_CONFIDENCE):
    return pyautogui.locateOnScreen(path, confidence=confidence)


def get_all_coordinates_by_image(path: str, confidence=DEFAULT_CONFIDENCE):
    """
    Returns all coordinates of matched images
    """
    found_images = [pyautogui.center(pos) for pos in _locate_all(path, confidence=confidence)]
    logger.info(f"Found images: {found_images}")
    return found_images


def get_coordinates_by_image(path: str, confidence=DEFAULT_CONFIDENCE, point="center"):
    locate = _locate_one(path, confidence)
    if point == "center":
        coordinates = pyautogui.center(locate)
    elif point == "top-left":
        coordinates = pyautogui.Point(locate.left, locate.top)
    elif point == "top-right":
        coordinates = pyautogui.Point(locate.left + locate.width, locate.top)
    else:
        raise ValueError(f"Unknown point: {point}")
    return coordinates


def click_by_image(path: str, confidence=DEFAULT_CONFIDENCE):
    """
    Click on the first found image
    """
    logger.info(f"Click by image {path}")
    coordinates = pyautogui.locateCenterOnScreen(path, confidence=confidence)
    if coordinates:
        logger.info(f"Coordinates: {coordinates}")
        click(*coordinates)
    else:
        raise pyautogui.ImageNotFoundException("Image not found!")


def click_all_by_image(path: str, confidence=DEFAULT_CONFIDENCE, limit=None):
    """
    Click on all found images or no more than limit times if it sets
    Returns number of found images
    """
    coordinates_list = get_all_coordinates_by_image(path, confidence)
    for i in range(len(coordinates_list)):
        if limit is not None and i >= limit:
            break
        click(*coordinates_list[i])
    return len(coordinates_list)


def get_screenshot():
    return pyautogui.screenshot()


def wait_and_click_by_image(path: str, confidence=DEFAULT_CONFIDENCE, timeout=5, count=1):
    logger.info(f"Wait and click by image {path}")
    end_time = time.time() + timeout
    while time.time() < end_time:
        coordinates = pyautogui.locateCenterOnScreen(path, confidence=confidence)
        if coordinates:
            logger.info(f"Click by coordinates: {coordinates} - {count} time(s)")
            for i in range(count):
                click(*coordinates)
            break
    else:
        raise pyautogui.ImageNotFoundException(f"Image {path} was not found after {timeout} seconds!")


def wait_and_click_by_image_ignoring_errors(path: str, confidence=DEFAULT_CONFIDENCE, timeout=0.1, count=1):
    try:
        wait_and_click_by_image(path, confidence, timeout, count)
        return True
    except pyautogui.ImageNotFoundException:
        return False


def wait_and_click_on_any_image(paths: List[str], confidence=DEFAULT_CONFIDENCE, timeout=5):
    logger.info(f"Wait and click on any image {paths}")
    end_time = time.time() + timeout
    while time.time() < end_time:
        for path in paths:
            coordinates = pyautogui.locateCenterOnScreen(path, confidence=confidence)
            if coordinates:
                logger.info(f"Click by image {path}")
                logger.info(f"Coordinates: {coordinates}")
                click(*coordinates)
                return
    raise pyautogui.ImageNotFoundException(f"Images {paths} were not found after {timeout} seconds!")


def is_image_present(path, confidence=DEFAULT_CONFIDENCE):
    coordinates = pyautogui.locateCenterOnScreen(path, confidence=confidence)
    is_present = True if coordinates else False
    logger.info(f"Image {path} visibility: {is_present}")
    return is_present


def wait_for_image(path, confidence=DEFAULT_CONFIDENCE, timeout=5):
    logger.info(f"Wait for image {path}")
    end_time = time.time() + timeout
    while time.time() < end_time:
        if is_image_present(path, confidence=confidence):
            break
    else:
        raise pyautogui.ImageNotFoundException(f"Image {path} was not found after {timeout} seconds!")


def is_image_present_wait(path, confidence=DEFAULT_CONFIDENCE, timeout=5):
    try:
        wait_for_image(path, confidence, timeout)
        return True
    except pyautogui.ImageNotFoundException:
        return False


def wait_for_no_image(path, confidence=DEFAULT_CONFIDENCE, timeout=5, exception=True):
    logger.info(f"Wait for no image {path}")
    end_time = time.time() + timeout
    while time.time() < end_time:
        if not is_image_present(path, confidence=confidence):
            break
    else:
        raise pyautogui.ImageNotFoundException(f"Image {path} was found after {timeout} seconds!")
