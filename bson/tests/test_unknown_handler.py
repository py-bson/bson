#!/usr/bin/env python

from bson import dumps, loads
from decimal import Decimal
from unittest import TestCase

class TestUnknownHandler(TestCase):
    def test_unknown_handler(self):
        d = Decimal("123.45")
        obj = {"decimal": d}

        serialized = dumps(obj, on_unknown=float)
	unserialized = loads(serialized)
	self.assertEqual(float(d), unserialized["decimal"])

