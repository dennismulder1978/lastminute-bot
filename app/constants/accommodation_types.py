"""
HolidayHunter standaard accommodatietypen.

Deze constante waarden worden gebruikt in:
- Deal.accommodation_type
- config.yaml
- DealFilter

Iedere scraper vertaalt provider-specifieke namen naar deze standaard.
"""

MOBILE_HOME = "mobile_home"
SAFARI_TENT = "safari_tent"
GLAMPING_TENT = "glamping_tent"
LODGE_TENT = "lodge_tent"
TENT = "tent"

LODGE = "lodge"
CHALET = "chalet"
BUNGALOW = "bungalow"
VILLA = "villa"
HOLIDAY_HOME = "holiday_home"
APARTMENT = "apartment"
HOTEL_ROOM = "hotel_room"
STUDIO = "studio"
SUITE = "suite"
BEACHHOUSE = "beach_house"

PITCH = "pitch"
CAMPING_PITCH = "camping_pitch"
MOTORHOME_PITCH = "motorhome_pitch"

TREEHOUSE = "treehouse"
CABIN = "cabin"
TINY_HOUSE = "tiny_house"
HOUSEBOAT = "houseboat"
YURT = "yurt"
TIPI = "tipi"
BELL_TENT = "bell_tent"
CARAVAN = "caravan"

OTHER = "other"


ALL_TYPES = [
    MOBILE_HOME,
    SAFARI_TENT,
    GLAMPING_TENT,
    LODGE_TENT,

    LODGE,
    CHALET,
    BUNGALOW,
    VILLA,
    HOLIDAY_HOME,
    APARTMENT,
    HOTEL_ROOM,
    STUDIO,
    SUITE,
    BEACHHOUSE,

    PITCH,
    CAMPING_PITCH,
    MOTORHOME_PITCH,

    TREEHOUSE,
    CABIN,
    TINY_HOUSE,
    HOUSEBOAT,
    YURT,
    TIPI,
    BELL_TENT,
    CARAVAN,

    OTHER,
]