# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 20:22:16 2022

@author: Hedi
"""
from .__colors__ import __colors__
def _set_color(x,col):
    return "".join((col,x,__colors__.color_off))
def _set_decimals(val,dec):
    return "".join(("{:.",dec,"f}")).format(val)
def _undefined():
    return _set_color("undefined",__colors__.bred)
def _callable():
    return _set_color("callable",__colors__.bcyan)
def _outbounds(val=""):
    return _set_color(str(val)+": outbounds",__colors__.bred)

def _is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`, 
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True