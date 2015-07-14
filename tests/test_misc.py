# -*- coding: utf-8 -*-

"""
Tests for misc functions.

"""

from nose.tools import *

from tsip.misc import b0, b1, b2, b3, b4, b5, b6, b7
from tsip.misc import b012, b4567

class TestBitExtraction(object):
    
    def test_b0(self):
        assert b0(0b00000001) == 1
        assert b0(0b00000000) == 0
        
    def test_b1(self):
        assert b1(0b00000010) == 1
        assert b1(0b00000000) == 0
        
    def test_b2(self):
        assert b2(0b00000100) == 1
        assert b2(0b00000000) == 0
        
    def test_b3(self):
        assert b3(0b00001000) == 1
        assert b3(0b00000000) == 0
        
    def test_b4(self):
        assert b4(0b00010000) == 1
        assert b4(0b00000000) == 0
        
    def test_b5(self):
        assert b5(0b00100000) == 1
        assert b5(0b00000000) == 0
        
    def test_b6(self):
        assert b6(0b01000000) == 1
        assert b6(0b00000000) == 0
        
    def test_b7(self):
        assert b7(0b10000000) == 1
        assert b7(0b00000000) == 0
        
    def test_b012(self):
        assert b012(0b00000000) == 0
        assert b012(0b00000001) == 1
        assert b012(0b00000010) == 2
        assert b012(0b00000011) == 3
        assert b012(0b00000100) == 4
        assert b012(0b00000101) == 5
        assert b012(0b00000110) == 6
        assert b012(0b00000111) == 7
        assert b012(0b11111000) == 0
        
    def test_b4567(self):
        assert b4567(0b00000000) == 0
        assert b4567(0b00010000) == 1
        assert b4567(0b00100000) == 2
        assert b4567(0b00110000) == 3
        assert b4567(0b01000000) == 4
        assert b4567(0b01010000) == 5
        assert b4567(0b01100000) == 6
        assert b4567(0b01110000) == 7
        assert b4567(0b10000000) == 8
        assert b4567(0b10010000) == 9
        assert b4567(0b10100000) == 10
        assert b4567(0b10110000) == 11
        assert b4567(0b11000000) == 12
        assert b4567(0b11010000) == 13
        assert b4567(0b11100000) == 14
        assert b4567(0b11110000) == 15
        assert b4567(0b00001111) == 0