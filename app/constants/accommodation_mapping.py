from app.constants import accommodation_types as hh

ROAN_MAPPING = {
    "stacaravans": hh.MOBILE_HOME,
    "safaritenten": hh.SAFARI_TENT,
    "lodges": hh.LODGE,
    "bungalows": hh.BUNGALOW,
    "kampeerplaatsen": hh.CAMPING_PITCH,
}

EUROCAMP_MAPPING = {
    # Mobile homes
    "mobile home": hh.MOBILE_HOME,

    # Tenten
    "tent": hh.TENT,
    "eco lodge tent": hh.LODGE,
    "safari tent": hh.SAFARI_TENT,
    "glamping tent": hh.GLAMPING_TENT,

    # Lodges / Chalets
    "lodge": hh.LODGE,
    "chalet": hh.CHALET,

    # Appartementen
    "apartment": hh.APARTMENT,
    "studio": hh.APARTMENT,
    "suite": hh.APARTMENT,

    # Huizen
    "villa": hh.VILLA,
    "bungalow": hh.BUNGALOW,
}

ROOMPOT_MAPPING = {
    "Safaritent 4": hh.SAFARI_TENT,
    "saft4": hh.SAFARI_TENT,
    "KVR5 Comfort": hh.MOBILE_HOME,
    "KVR5": hh.MOBILE_HOME,
    "Comfort 6 ": hh.MOBILE_HOME,
    "comfort6": hh.MOBILE_HOME,
    "comf6": hh.MOBILE_HOME,
    "Beach House ": hh.BEACHHOUSE,
    "4-6 beach46": hh.BEACHHOUSE,
    "beach46" : hh.BEACHHOUSE,
    "Penthouse 6 ": hh.VILLA,
    "pent6": hh.VILLA,
    "Villa 6A ": hh.VILLA,
    "ca6a": hh.VILLA,
    "bung": hh.BUNGALOW,
    "achaletnotaris4": hh.BUNGALOW,
    "Lightadv": hh.LODGE,
    "2-4-person ": hh.MOBILE_HOME,
    "outdoor tiny ": hh.MOBILE_HOME,
    "house 2-4BE": hh.MOBILE_HOME,
    "2-4BE": hh.MOBILE_HOME,
    "4-person ": hh.LODGE,
    "Lodge 4B3": hh.LODGE,
    "4B3": hh.BUNGALOW,
    "4-person ": hh.GLAMPING_TENT,
    "Glampingtent ": hh.GLAMPING_TENT,
    "4ST": hh.GLAMPING_TENT,
    "seahousecom" : hh.MOBILE_HOME,
    # nieuw
    "comfvilla4": hh.VILLA,
    "ca4gcomfort": hh.BUNGALOW,
    "fv12com": hh.BUNGALOW,
    "kvr5": hh.BUNGALOW,
    "lodge4": hh.VILLA,
    "for4": hh.BEACHHOUSE,
    "y": hh.YURT,
    "lightadv": hh.LODGE,
    "2-4be": hh.BUNGALOW,
    "4b3": hh.BUNGALOW,
    "4st": hh.GLAMPING_TENT,
    "4b2": hh.VILLA,
}

LANDAL_MAPPING = {
    "6c4": hh.BUNGALOW,
    "4b5": hh.BUNGALOW,
    "4b1": hh.BUNGALOW,
    "4c": hh.BUNGALOW,
    "4ca": hh.BUNGALOW,
    "4c1": hh.BUNGALOW,
    "4cp10": hh.BUNGALOW,
    "6b": hh.BUNGALOW,
    "4cp9": hh.BUNGALOW,

}

TWENTY_MAPPING = {
    'safari-tents': hh.TENT,
    'lodge-tent': hh.LODGE_TENT,
    'mobile-home': hh.MOBILE_HOME,
    'bungalow-tent': hh.TENT,
    'pitch': hh.PITCH,
    'apartment': hh.APARTMENT,

}

