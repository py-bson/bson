#!/usr/bin/env python

from bson import dumps, loads
from unittest import TestCase
import pytz
from datetime import datetime

class TestDateTime(TestCase):
	def test_datetime(self):
		now = datetime.now(pytz.utc)
		obj = {"now" : now}
		serialized = dumps(obj)
		obj2 = loads(serialized)

		td = obj2["now"] - now
		seconds_delta = (td.microseconds + (td.seconds + td.days * 24 * 3600) *
				1e6) / 1e6
		self.assertTrue(abs(seconds_delta) < 0.001)
