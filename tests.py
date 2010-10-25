import bson
import unittest

class DocumentCodecTestCase(unittest.TestCase):

	def setUp(self):
		super(DocumentCodecTestCase, self).setUp()
		self.codec = bson.DocumentCodec()

	def check_codec(self, val):
		self.assertEqual(str(self.codec), val)
	
	def check_dict(self, val):
		length, decoded = bson.codec.decode_document(str(self.codec), 0)
		self.assertEqual(decoded, val)

	def test_ordered_write_way_one(self):
		self.codec['first_name'] = 'alan'
		self.codec['last_name'] = 'turing'
		self.check_codec('0\x00\x00\x00\x05first_name\x00\x04\x00\x00\x00\x00alan\x05last_name\x00\x06\x00\x00\x00\x00turing\x00')
		self.check_dict({'first_name': 'alan', 'last_name': 'turing'})

	def test_ordered_write_way_two(self):
		self.codec['last_name'] = 'turing'
		self.codec['first_name'] = 'alan'
		self.check_codec('0\x00\x00\x00\x05last_name\x00\x06\x00\x00\x00\x00turing\x05first_name\x00\x04\x00\x00\x00\x00alan\x00')
		self.check_dict({'first_name': 'alan', 'last_name': 'turing'})

	def test_ordered_dict_write_one(self):
		self.codec['first_name'] = 'alan'
		self.codec['last_name'] = 'turing'
		with self.codec.dict_ctx('dates') as c:
			c['birth'] = '1912-06-23'
			c['death'] = '1954-06-07'
		self.check_codec('h\x00\x00\x00\x05first_name\x00\x04\x00\x00\x00\x00alan\x05last_name\x00\x06\x00\x00\x00\x00turing\x03dates\x001\x00\x00\x00\x05birth\x00\n\x00\x00\x00\x001912-06-23\x05death\x00\n\x00\x00\x00\x001954-06-07\x00\x00')
		self.check_dict({'first_name': 'alan', 'last_name': 'turing', 'dates': {'birth': '1912-06-23', 'death': '1954-06-07'}})

	def test_ordered_dict_write_two(self):
		self.codec['first_name'] = 'alan'
		self.codec['last_name'] = 'turing'
		with self.codec.dict_ctx('dates') as c:
			c['death'] = '1954-06-07'
			c['birth'] = '1912-06-23'
		self.check_codec('h\x00\x00\x00\x05first_name\x00\x04\x00\x00\x00\x00alan\x05last_name\x00\x06\x00\x00\x00\x00turing\x03dates\x001\x00\x00\x00\x05death\x00\n\x00\x00\x00\x001954-06-07\x05birth\x00\n\x00\x00\x00\x001912-06-23\x00\x00')
		self.check_dict({'first_name': 'alan', 'last_name': 'turing', 'dates': {'birth': '1912-06-23', 'death': '1954-06-07'}})

if __name__ == '__main__':
	unittest.main()
