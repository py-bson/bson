from unittest import TestCase

from bson import dumps, loads
import json

class TestIntAsKey(TestCase):
    def setUp(self):
        self.test_dict = {
            10: 'pass?',
            10.2: 'pass?'
        }
    
    def test_int_as_key(self):
        dump = dumps(self.test_dict)
        decoded = loads(dump)
        dumpByJson = json.dumps(self.test_dict)
        decodedByJson = json.loads(dumpByJson)
        self.assertEqual(decoded, decodedByJson)


