#!/usr/bin/env python
from decimal import Decimal

from unittest import TestCase

from bson import dumps, loads


class TestDecimal(TestCase):
    def test_decimal(self):
        decimal = Decimal('1234.45')
        obj = {"decimal": decimal}
        serialized = dumps(obj)
        obj2 = loads(serialized)

        self.assertIsInstance(obj2['decimal'], float)
        self.assertTrue(obj2['decimal'] == float(decimal))
