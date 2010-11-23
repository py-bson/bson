#!/usr/bin/env python

from bson import BSONCoding, dumps, loads, import_class
from unittest import TestCase

class TestData(BSONCoding):
	def __init__(self, *args):
		self.args = args

	def bson_encode(self):
		return {"args" : self.args}

	def bson_init(self, raw_values):
		self.args = raw_values["args"]

	def __eq__(self, other):
		if not isinstance(other, TestData):
			return NotImplemented
		args = other.args
		if len(self.args) != len(args):
			return False

		for i in xrange(0, len(self.args)):
			if self.args[i] != args[i]:
				return False

		return True

class TestObjectCoding(TestCase):
	def test_codec(self):
		import_class(TestData)
		data = TestData(u"Lorem ipsum dolor sit amet",
				"consectetur adipisicing elit",
				42)
		serialized = dumps(data)
		data2 = loads(serialized)
		self.assertTrue(data == data2)
