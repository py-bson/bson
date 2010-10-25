try:
	import cStringIO as StringIO
except ImportError:
	import StringIO

import struct
from contextlib import contextmanager
from bson import codec

class DocumentCodec(object):
	"""This is an alternative version of codec.encode_document that allows
	control over the order in which elements are serialized. This may be
	important because some applications (e.g. MongoDB) could expect an ordering
	on the keys within "documents" (i.e. dictionaries).
	"""

	def __init__(self, **kw):
		self.buf = StringIO.StringIO()
		for k, v in kw.iteritems():
			self[k] = v

	def encode_element(self, name, value):
		if isinstance(value, float):
			self.buf.write(codec.encode_double_element(name, value))
		elif isinstance(value, unicode):
			self.buf.write(codec.encode_string_element(name, value))
		elif isinstance(value, dict):
			self.buf.write(codec.encode_document_element(name, value))
		elif isinstance(value, list) or isinstance(value, tuple):
			self.buf.write(codec.encode_array_element(name, value))
		elif isinstance(value, str):
			self.buf.write(codec.encode_binary_element(name, value))
		elif isinstance(value, bool):
			self.buf.write(codec.encode_boolean_element(name, value))
		elif value is None:
			self.buf.write(codec.encode_none_element(name, value))
		elif isinstance(value, int):
			self.buf.write(codec.encode_int32_element(name, value))
		elif isinstance(value, long):
			self.buf.write(codec.encode_int64_element(name, value))

	@contextmanager
	def dict_ctx(self, name):
		"""Yield a sub-DocumentCodec, which also allows ordered writes"""
		self.buf.write('\x03' + name)
		inner_doc = DocumentCodec()
		yield inner_doc
		self.buf.write(str(inner_doc))

	def __setitem__(self, name, value):
		self.encode_element(name, value)

	def __str__(self):
		e_list = self.buf.getvalue()
		e_list_length = len(e_list)
		return struct.pack("<i%dsb" % (e_list_length,), e_list_length + 4 + 1, e_list, 0)

	def __repr__(self):
		return repr(str(self))

__all__ = ['DocumentCodec']
