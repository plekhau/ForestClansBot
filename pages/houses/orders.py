import logging
import time

from constants import (img_house_orders_logo_ready, img_house_orders_order_ready, img_house_orders_send,
                       img_house_orders_title)
from helpers.images import wait_and_click_by_image, wait_and_click_by_image_ignoring_errors, wait_for_image

logger = logging.getLogger(__name__)


def open_orders_if_ready() -> bool:
    """
    Opens orders and returns True if completed orders are present.
    Otherwise, returns False
    """
    if wait_and_click_by_image_ignoring_errors(img_house_orders_logo_ready):
        wait_for_image(img_house_orders_title)
        return True
    return False


# def close_orders() -> None:
#     """
#     Close Orders popup
#     """
#     wait_and_click_by_image(img_house_orders_send)


def send_ready_order() -> None:
    """
    Sends ready order.
    """
    wait_and_click_by_image(img_house_orders_order_ready)
    wait_and_click_by_image(img_house_orders_send)
    time.sleep(5)


def send_all_ready_orders() -> None:
    """
    Opens Orders if ready orders are present, sends them
    """
    logger.info("Send all ready orders")
    while open_orders_if_ready():
        send_ready_order()
