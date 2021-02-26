# -*- coding: utf-8 -*-
import os
import sys

def limpar_string(text, allowed):
    r = ""
    for k in text:
        if k in allowed:
            r += k
    return r

def apenas_numeros(text):
    return limpar_string(text, '0123456789')