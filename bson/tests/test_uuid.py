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

    def test_legacy_uuid(self):
        uuid = UUID('584bcd8f-6d81-485a-bac9-629c14b53847')
        serialized = b' \x00\x00\x00\x05uuid\x00\x10\x00\x00\x00\x03XK\xcd\x8fm\x81HZ\xba\xc9b\x9c\x14\xb58G\x00'
        obj = loads(serialized)

        self.assertIsInstance(obj['uuid'], UUID)
        self.assertTrue(obj['uuid'] == uuid)
