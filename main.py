import logging
from time import sleep

import arrow

from config import ALLOWED_POTIONS, COOKING, LOOPS_TO_COOK, LOOPS_TO_SELL, MAX_POTIONS
from constants import LABORATORY_CONTAINER
from helpers.common import countdown, get_hike_delay, repeat_if_return_to_game_error, restart_app, teardown
from pages.houses.basket import sell_mushrooms
from pages.houses.laboratory import create_potions
from pages.houses.orders import send_all_ready_orders
from pages.houses.production import cook_all_productions
from pages.mail_page import go_hike_from_mails
from pages.main_page import (Status, game_preparation, go_hike, is_antidote_activated, is_container_activated,
                             is_hike_available, pick_up_all_mushrooms, pick_up_products, set_minimum_scale)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log", mode="w"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


@repeat_if_return_to_game_error
def main(max_field=None, restart=False, potion=False):
    loops = {"sell": 0, "cook": 0}
    force_hike = False
    mails_have_hike = True
    next_hike_time = arrow.now()
    while True:
        loops["sell"] += 1
        loops["cook"] += 1
        status = game_preparation()
        if status["mushrooms_stolen"]:
            mails_have_hike = True

        # Check antidote
        antidote = is_antidote_activated()

        # Hike
        now = arrow.now()
        result = go_hike(max_field=max_field, potion=potion, force_hike=force_hike, antidote=antidote)
        hike_status = result["status"]
        logger.info(f"Hike status: {hike_status}")
        if hike_status != Status.NO_HIKE:
            next_hike_time = now.shift(seconds=get_hike_delay(result["fields"]))

        # Check if needed to force next hike
        force_hike = True if hike_status == Status.OK_SANDWICH else False

        # Create potions
        set_minimum_scale()
        if potion and ALLOWED_POTIONS and hike_status not in (Status.NO_HIKE, Status.OK_NOTHING_TO_PICK_UP):
            # Check container
            container = is_container_activated()

            max_potions = MAX_POTIONS + LABORATORY_CONTAINER if container else MAX_POTIONS
            create_potions({ALLOWED_POTIONS[0]: max_potions})

        if hike_status in (Status.NO_SPACE,):
            break

        # Hike from mails
        is_hike_from_emails = False
        if mails_have_hike:
            hike_status = go_hike_from_mails(max_field=None, potion=potion, antidote=antidote)
            if not isinstance(hike_status, bool):
                is_hike_from_emails = True
                loops["sell"] += 1
                loops["cook"] += 1

                # Create potions
                set_minimum_scale()
                if potion and ALLOWED_POTIONS and hike_status not in (Status.OK_NOTHING_TO_PICK_UP, ):
                    # Check container
                    container = is_container_activated()

                    max_potions = MAX_POTIONS + LABORATORY_CONTAINER if container else MAX_POTIONS
                    create_potions({ALLOWED_POTIONS[0]: max_potions})

                if hike_status in (Status.NO_SPACE,):
                    break
            else:
                mails_have_hike = hike_status

        # Pick up our mushrooms
        if not force_hike and not is_hike_from_emails and pick_up_all_mushrooms(antidote=antidote)["status"] not in (
            Status.OK,
            Status.OK_NOTHING_TO_PICK_UP,
        ):
            break

        # Pick up all ready products
        pick_up_products()

        # Send ready orders if needed
        send_all_ready_orders()

        # Cooking
        if COOKING and loops["cook"] >= LOOPS_TO_COOK:
            cook_all_productions()
            loops["cook"] = 0

        # Sell mushrooms
        if LOOPS_TO_SELL and loops["sell"] >= LOOPS_TO_SELL:
            sell_mushrooms(True)
            loops["sell"] = 0

        # Skip pause if hike is already available
        if force_hike or is_hike_available():
            continue

        now = arrow.now()
        if restart and now.shift(minutes=10) < next_hike_time:
            restart_app(10)
        elif now.shift(minutes=5) < next_hike_time:
            countdown(5)
        else:
            time_to_wait = (next_hike_time - now).seconds if next_hike_time > now else 0
            logger.info(f"Wait for: {time_to_wait} seconds")
            sleep(time_to_wait)


if __name__ == "__main__":
    try:
        main(restart=False, potion=False)
    except Exception as ex:
        teardown()
        raise ex
