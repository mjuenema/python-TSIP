# -*- coding: utf-8 -*-

"""
Misc functions.

"""


def b0(data):
    return data & 0b00000001

def b1(data):
    return (data & 0b00000010) >> 1

def b2(data):
    return (data & 0b00000100) >> 2

def b3(data):
    return (data & 0b00001000) >> 3

def b4(data):
    return (data & 0b00010000) >> 4

def b5(data):
    return (data & 0b00100000) >> 5

def b6(data):
    return (data & 0b01000000) >> 6

def b7(data):
    return (data & 0b10000000) >> 7

def b012(data):
    return data & 0b00000111

def b4567(data):
    return (data & 0b11110000) >> 4 