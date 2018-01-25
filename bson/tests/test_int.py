#!/usr/bin/env python
from unittest import TestCase

from bson import dumps, loads


class TestInt(TestCase):
    def setUp(self):
        self.good_rquest_dict = {
            "uint64": 0xFFFFFFFFFFFFFFFF - 1,
            "int64:": 0x7FFFFFFFFFFFFFFF - 1,
            "int32": 0x7fffffff
        }
        self.bad_request_dict = {
            "uint64": 0xFFFFFFFFFFFFFFFF << 1
        }

    def test_int(self):
        dump = dumps(self.good_rquest_dict)
        decoded = loads(dump)
        self.assertEqual(decoded, self.good_rquest_dict)

        with self.assertRaises(Exception):
            dump = dumps(self.bad_request_dict)
            decoded = loads(dump)
