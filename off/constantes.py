#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""
Program constantes.
"""
from stop_words import get_stop_words

STOP_WORDS = get_stop_words("fr")
NO_CHARS_LIST = [
    "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "[", "]",
    "{", "}", ";", ":", ",", ".", "/", "<", ">", "?", "|", "`",
    "~", "-", "=", "_", "+", "&", "'", "§", "°", "^", "¨", "%",
    "`", "£", "-", "_"
]
CATEGORIES = (
    "Biscuits",
    "Boissons",
    "Desserts",
    "Epiceries",
    "Féculents",
    "Fromages",
    "Gateaux",
    "Légumes",
    "Poissons",
    "Viandes"
)
URL_BEGIN = 'https://fr.openfoodfacts.org/cgi/search.pl'
P_SIZE = 20

# KEYS_API = (
#     ['product_name_fr'],
#     ['image_url'],
#     ['id'],
#     ['nutriscore_grade'],
#     (['nutriments']['proteins']),
#     (['nutriments']['salt']),
#     (['nutriments']['fat']),
#     (['nutriments']['sugars']),
#     (['nutriments']['carbohydrates']),
#     ['url']
# )
