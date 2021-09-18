from constants import Potions

MY_MAX_FIELD = 17
MAX_POTIONS = 10

# how many attempt we have for each field. It depends on mushroom level in school.
# If field value is not set (mushroom is not investigated in school) -> default value 14 will be used
# This affects fast picking up mushroom: pick up <value - 3> mushroom without additions checks
FIELD_ATTEMPTS = {
    1: 28,
    2: 28,
    3: 28,
    4: 28,
    5: 28,
    6: 29,
    7: 29,
    8: 30,
    9: 30,
    10: 30,
    11: 30,
    12: 31,
    13: 31,
    14: 31,
    15: 30,
    16: 30,
    17: 30,
    18: 17,
}

# List of potions that can be used for picking up mushrooms
# It is applied according to the order in this list
ALLOWED_POTIONS = [Potions.ABSOLUT, Potions.ENERGY, Potions.LUCK]
# ALLOWED_POTIONS = [Potions.ENERGY]
# ALLOWED_POTIONS = [Potions.LUCK]
# ALLOWED_POTIONS = [Potions.HARVEST]

# Fields whose mushrooms will not be sold.
# Usually it's explored fields + most expensive mushrooms which can be processed
# LIMIT: no more than 14 fields (15 slots in a basket)
# FIELDS_NOT_FOR_SALE = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
FIELDS_NOT_FOR_SALE = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38]
assert len(FIELDS_NOT_FOR_SALE) < 15

# Allows to ignore FIELDS_NOT_FOR_SALE setting and not to sell mushrooms at all if it's True
NO_SALE = True

# the field from which all fields will be collected in hike and a sandwich will be eaten after that
# Need for tournament only
# Use None to disable this option
SANDWICH_FIELD = None

# The first field to pick up mushrooms in hike.
# Useful to set it as MY_MAX_FIELD + 1 to reduce your rating
HIKE_START_FIELD = 1

# Amount of all products (Drier, Barrel, etc.)
PRODUCT_AMOUNT = 24

# Allow cooking automatically
COOKING = True

# Cooking is happened after this amount of loops
LOOPS_TO_COOK = 1

# Sell mushrooms after this amount of loops.
# Set 0 to forbid selling.
LOOPS_TO_SELL = 3

# Promotions
# Toadstool has no effect
PROMOTION_NO_TOADSTOOL = False

