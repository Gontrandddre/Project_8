#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""
Program constantes.
"""
from stop_words import get_stop_words

STOP_WORDS = get_stop_words("fr")
NO_CHARS_LIST = [
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
    ";",
    ":",
    ",",
    ".",
    "/",
    "<",
    ">",
    "?",
    "|",
    "`",
    "~",
    "-",
    "=",
    "_",
    "+",
    "&",
    "'",
    "§",
    "°",
    "^",
    "¨",
    "%",
    "`",
    "£",
    "-",
    "_",
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
    "Viandes",
    "Snacks",
    "Sauces",
    "Pains",
    "Fromages",
    "Huiles",
    "Charcuteries",
    "Produits laitiers",
    "Pates à tartiner"
)
URL_BEGIN = "https://fr.openfoodfacts.org/cgi/search.pl"
