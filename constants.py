import os

PROJECT_DIR = os.path.dirname(__file__)
PATH_TO_IMAGES = os.path.join(PROJECT_DIR, "images/")

MAX_FIELD = 38

PATH_TO_APP = "C:/Users/Alex/AppData/Local/Programs/ForestClans/ForestClans.exe"

DEFAULT_FIELD_ATTEMPTS = 14  # Attempts to pick up mushrooms https://gribniki.fandom.com/ru/wiki/Школа_и_изучения
LUCK_POTION_ATTEMPTS = 35  # Attempts after using Luck potion
ENERGY_POTION_ATTEMPTS = 5  # Attempts after using Energy potion
TOADSTOOL_ATTEMPTS = 3  # Attempts reducing after toadstool
LABORATORY_CONTAINER = 4  # Additional poisons from container

img_system_window_maximize = PATH_TO_IMAGES + "system/window_maximize.png"

img_common_return_to_game = PATH_TO_IMAGES + "common/return_to_game.png"  # return to game button when game is not active long time
img_common_mushrooms_stolen = PATH_TO_IMAGES + "common/mushrooms_stolen.png"  # somebody stolen your mushrooms
img_common_mushrooms_stolen_ok = PATH_TO_IMAGES + "common/mushrooms_stolen_ok.png"  # OK button

img_field_logo = PATH_TO_IMAGES + "fields/{}/logo.png"  # mushroom icon on main screen
img_field_check = PATH_TO_IMAGES + "fields/{}/check.png"  # mushroom icon on field screen to check that screen is opened
img_field_hide_folder = PATH_TO_IMAGES + "fields/{}/hide/"  # images that hide mushrooms
img_field_finish = PATH_TO_IMAGES + "fields/finish.png"  # image that is shown at the end of picking up
img_field_finish_ok = PATH_TO_IMAGES + "fields/finish_ok.png"  # OK button for finish popup
img_field_return_to_home = PATH_TO_IMAGES + "fields/return_to_home.png"  # Return to main screen
img_field_left_arrow = PATH_TO_IMAGES + "fields/arrow_left.png"  # Previous field
img_field_right_arrow = PATH_TO_IMAGES + "fields/arrow_right.png"  # Next field
img_field_mushroom_rain = PATH_TO_IMAGES + "fields/mushroom_rain.png"  #
img_field_popup_no_space_label = PATH_TO_IMAGES + "fields/popup_no_space_label.png"  # Popup: you have no space
img_field_popup_no_space_go_home = PATH_TO_IMAGES + "fields/popup_no_space_go_home.png"  # Popup: go home button
img_field_star = PATH_TO_IMAGES + "fields/star.png"  # Only for hike, current progress (1-3 stars)
img_field_potions = PATH_TO_IMAGES + "fields/potions/"  # Potions
img_field_antidote = PATH_TO_IMAGES + "fields/antidote.png"  # Antidote
img_field_container = PATH_TO_IMAGES + "fields/container.png"  # Container

img_main_minus = PATH_TO_IMAGES + "main/minus.png"  # minimize scale
img_main_plus = PATH_TO_IMAGES + "main/plus.png"  # maximize scale
img_main_in_hike = PATH_TO_IMAGES + "main/in_hike.png"  # In Hike!
img_main_in_hike_force = PATH_TO_IMAGES + "main/in_hike_force.png"  # Part of hike image which is always present
img_main_in_hike_force_apply = PATH_TO_IMAGES + "main/in_hike_force_apply.png"  # Apply hike with sandwich
img_main_hike_finish = PATH_TO_IMAGES + "main/hike_finish.png"  # Hike finish message
img_main_hike_finish_ok = PATH_TO_IMAGES + "main/hike_finish_ok.png"  # Ok button for Hike finish popup
img_main_hike_popup_remove_def_title = PATH_TO_IMAGES + "main/popup_remove_def_title.png"  # Popup: remove defence
img_main_hike_popup_remove_def_ok = PATH_TO_IMAGES + "main/popup_remove_def_ok.png"  # Popup: remove defence - OK
img_main_hike_popup_remove_def_no = PATH_TO_IMAGES + "main/popup_remove_def_no.png"  # Popup: remove defence - Cancel
img_main_products_ready = PATH_TO_IMAGES + "main/products/ready/"  # Products icons to pick up
img_main_mail = PATH_TO_IMAGES + "main/mail.png"  # Popup: remove defence - Cancel


img_hike_go_home = PATH_TO_IMAGES + "hike/go_home.png"  # Go home button

# Houses
# Basket
img_house_basket_logo = PATH_TO_IMAGES + "houses/basket/logo.png"  # Basket on main screen
img_house_basket_menu_mushrooms = PATH_TO_IMAGES + "houses/basket/menu_mushrooms.png"  # Menu: open basket
img_house_basket_popup_title = PATH_TO_IMAGES + "houses/basket/popup_title.png"  # Title of opened basket
img_house_basket_popup_sell = PATH_TO_IMAGES + "houses/basket/popup_sell.png"  # Sell button
img_house_basket_popup_empty_basket = PATH_TO_IMAGES + "houses/basket/popup_empty_basket.png"  # Basket is empty
img_house_basket_popup_empty_slot = PATH_TO_IMAGES + "houses/basket/popup_empty_slot.png"  # Empty slot of basket
img_house_basket_popup_close = PATH_TO_IMAGES + "houses/basket/popup_close.png"  # Close icon
img_house_basket_mushroom = PATH_TO_IMAGES + "houses/basket/mushrooms/{}.png"  # Title of opened basket

# Orders
img_house_orders_logo_ready = PATH_TO_IMAGES + "houses/orders/logo_ready.png"  # Ready orders on main screen
img_house_orders_title = PATH_TO_IMAGES + "houses/orders/title.png"  # Any element on Orders popup to check if popup is present
img_house_orders_order_ready = PATH_TO_IMAGES + "houses/orders/order_ready.png"  # Order with green mark
img_house_orders_send = PATH_TO_IMAGES + "houses/orders/send.png"  # Send button

# Laboratory
img_house_laboratory_logo = PATH_TO_IMAGES + "houses/laboratory/logo.png"  # Laboratory on main screen
img_house_laboratory_menu_create_potion = PATH_TO_IMAGES + "houses/laboratory/menu_create_potion.png"  # Menu: open Lab
img_house_laboratory_popup_title = PATH_TO_IMAGES + "houses/laboratory/popup_title.png"  # Title of opened Laboratory
img_house_laboratory_popup_close = PATH_TO_IMAGES + "houses/laboratory/popup_close.png"  # Close icon
img_house_laboratory_popup_potions = PATH_TO_IMAGES + "houses/laboratory/potions/"  # Close icon

# Production
img_house_production_logos = PATH_TO_IMAGES + "houses/production/logos/"  # Productions on main screen
img_house_production_menu_cook = PATH_TO_IMAGES + "houses/production/menu_cook.png"  # Menu: open Cooking
img_house_production_popup_close = PATH_TO_IMAGES + "houses/production/popup_close.png"  # Close icon
img_house_production_popup_right_arrow = PATH_TO_IMAGES + "houses/production/popup_right_arrow.png"  # Next product
img_house_production_popup_left_arrow = PATH_TO_IMAGES + "houses/production/popup_left_arrow.png"  # Previous product
img_house_production_popup_left_conner = PATH_TO_IMAGES + "houses/production/popup_left_conner.png"  # Left conner of info block
img_house_production_popup_right_conner = PATH_TO_IMAGES + "houses/production/popup_right_conner.png"  # Right conner of info block

# Mail
MAIL_PAGES_AMOUNT = 7
img_mail_arrow_left = PATH_TO_IMAGES + "mail/arrow_left.png"  # Left arrow
img_mail_arrow_right = PATH_TO_IMAGES + "mail/arrow_right.png"  # Right arrow
img_mail_close = PATH_TO_IMAGES + "mail/close.png"  # Close button
img_mail_hikes_to_you_tab_enabled = PATH_TO_IMAGES + "mail/hikes_to_you_tab_enabled.png"  # Enabled Hikes to you tab
img_mail_hikes_to_you_tab_disabled = PATH_TO_IMAGES + "mail/hikes_to_you_tab_disabled.png"  # Disabled Hikes to you tab
img_mail_go_hike = PATH_TO_IMAGES + "mail/go_hike.png"  # Go Hike button


# classes
class Potions:
    """
    Available potions. Names match image files.
    """
    ENERGY = "01_energy.png"
    HARVEST = "02_harvest.png"
    FORECAST = "03_forecast.png"
    LUCK = "04_luck.png"
    ABSOLUT = "05_absolut.png"
