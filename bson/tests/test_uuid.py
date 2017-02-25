#!/usr/bin/env python
from uuid import UUID

from unittest import TestCase

from bson import dumps, loads


class TestUUID(TestCase):
    def test_uuid(self):
        uuid = UUID('584bcd8f-6d81-485a-bac9-629c14b53847')
        obj = {"uuid": uuid}
        serialized = dumps(obj)
        obj2 = loads(serialized)

        self.assertIsInstance(obj2['uuid'], UUID)
        self.assertTrue(obj2['uuid'] == uuid)
