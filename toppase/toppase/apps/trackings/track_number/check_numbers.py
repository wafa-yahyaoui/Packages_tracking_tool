# -*- coding: utf-8 -*-
import re
from fedex import track_fedex
from ups import track_ups
from scraping_laposte_website import track_laposte

# fedex : 779608863132
# DHL :
# laposte :
# ups :
# collismo : 8N03669633565



fedex_pattern = ["^\d{12}$", "^\d{14}$", "^\d{15}$", "^\d{20}$", "^\d{22}$"]
ups_patter = ["^1Z\d{16}$", "^W\d{10}$", "^T\d{10}$", "^H\d{10}$"]
dhl_pattern = ["^\d{10}$"]
laposte_pattern = ["^\w{11,15}$"]

# TODO
# collismo_pattern =
# chronopost_pattern =

# list of all existing pattern
all_pattern = [fedex_pattern, dhl_pattern, laposte_pattern, ups_patter, ]


# tracking_number = "779608863132"


def fedex(tracking_number):
    JSON_response = track_fedex(tracking_number)
    return JSON_response


def dhl(tracking_number):
    pass


def laposte(tracking_number):
    JSON_response = track_laposte(tracking_number)
    return JSON_response

def ups(tracking_number):
    JSON_response = track_ups(tracking_number)
    return JSON_response


# def collismo(tracking_number):
#     pass
#
#
# def chronopost(tracking_number):
#     pass


poste = {0: fedex,
         1: dhl,
         2: laposte,
         3: ups,
         #4: collismo,
         #5: chronopost,
         }


def track(tracking_number):
    # goto prend une valeur parmis les valeurs du poste (dict) pour appeler la bonne api
    goto = None

    # len(all_pattern) correspond au nombres des api quant-à
    for indice in range(len(all_pattern)):
        result = [True for s in all_pattern[indice] if (re.match(pattern=s, string=str(tracking_number)) is not None)]
        goto = indice if len(result) == 1 else None
        if goto is not None:
            break
    if (goto is not None):
        # appel de la bonne api selon goto
        return poste[goto](tracking_number)
    else:
        # si la valeur du tracking_number ne correspond a aucune format des api disponibles
        # raise ValueError("Incorrect ID")
        return "Incorrect ID"