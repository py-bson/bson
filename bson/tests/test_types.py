#!/usr/bin/env python
from unittest import TestCase

from bson import dumps, loads
from bson.types import UInt64, Int64, Int32


class TestTypes(TestCase):
    def setUp(self):
        self.good_request_dict = {
            "uint64": UInt64(0xFFFFFFFFFFFFFFFF - 1),
            "int64": Int64(0x7FFFFFFFFFFFFFFF - 1),
            "int32": Int32(0x7fffffff)
        }

    def test_bad_values(self):
        with self.assertRaises(ValueError):
            UInt64(0xFFFFFFFFFFFFFFFF << 1)
        with self.assertRaises(ValueError):
            Int32(2**32)
        with self.assertRaises(ValueError):
            Int64(2**64)
        with self.assertRaises(ValueError):
            Int32(-2**31-1)
        with self.assertRaises(ValueError):
            Int64(-2**63-1)

    def test_int(self):
        dump = dumps(self.good_request_dict)
        decoded = loads(dump)
        self.assertEqual(decoded, {k: v.get_value() for k, v in self.good_request_dict.items()})

