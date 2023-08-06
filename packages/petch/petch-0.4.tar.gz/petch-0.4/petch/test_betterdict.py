from unittest import TestCase
from betterdict import BetterDict as BD


class TestBetterDict(TestCase):
    def test_keys_list(self):
        dict1 = BD({"a": 3, "b": 2, "c": 1})
        self.assertEqual(dict1.keys_list[0], "a")
