#!/usr/bin/env python
from unittest import TestCase

from bson import dumps, loads


class TestInt(TestCase):
    def setUp(self):
        self.goodRquestDict = {
            "uint64": 0xFFFFFFFFFFFFFFFF - 1,
            "int64:": 0x7FFFFFFFFFFFFFFF - 1,
            "int32": 0x7fffffff
        }
        self.badRequestDict = {
            "uint64": 0xFFFFFFFFFFFFFFFF << 1
        }

    def test_int(self):
        dump = dumps(self.goodRquestDict)
        decoded = loads(dump)
        self.assertEqual(decoded, self.goodRquestDict)

        with self.assertRaises(Exception):
            dump = dumps(self.badRequestDict)
            decoded = loads(dump)
