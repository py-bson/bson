#!/usr/bin/env python
from unittest import TestCase

from bson import dumps, loads


class TestNonUtf8Binary(TestCase):
    def setUp(self):
        self.doc = {b'\x88': None}

    def test_non_utf8_binary(self):
        dump = dumps(self.doc)
        decoded = loads(dump)
        self.assertEqual(decoded, self.doc)
