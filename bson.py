#!/usr/bin/python -OOOO
# vim: set fileencoding=utf8 shiftwidth=4 tabstop=4 textwidth=80 foldmethod=marker :
"""
BSON serialization and deserialization logic.
Specifications taken from: http://bsonspec.org/#/specification
The following types are unsupported, because for data exchange purposes, they're
over-engineered:
	0x06 (Undefined)
	0x07 (ObjectId)
	0x09 (UTC datetime - Sorry, but Python's datetime module sucks.
		datetime.now() has no timezone? Seriously?! Simple timestamps will save
		you a lot of trouble)
	0x0b (Regex - Exactly which flavor do you want? Better let higher level
		programmers make that decision.)
	0x0c (DBPointer)
	0x0d (JavaScript code)
	0x0e (Symbol)
	0x0f (JS w/ scope)
	0x11 (MongoDB-specific timestamp)

For binaries, only the default 0x0 type is supported.
"""

import struct
from cStringIO import StringIO

# {{{ Private Logic
def _encode_string(value):
	length = len(value)
	return struct.pack("<i%dsb" % (length,), length + 1, value, 0)

def _decode_string(data, base):
	length = struct.unpack("<i", data[base:base + 4])[0]
	value = data[base + 4: base + 4 + length - 1]
	return (base + 4 + length, value)

def _encode_cstring(value):
	return value + "\x00"

def _decode_cstring(data, base):
	buf = StringIO()
	length = 0
	for character in data[base:]:
		length += 1
		if character == "\x00":
			break
		buf.write(character)
	return (base + length, buf.getvalue())

def _encode_binary(value):
	length = len(value)
	return struct.pack("<ib", length, 0) + value

def _decode_binary(data, base):
	length, binary_type = struct.unpack("<ib", data[base:base + 5])
	return (base + 5 + length, data[base + 5:base + 5 + length])

def _encode_double(value):
	return struct.pack("<d", value)

def _decode_double(data, base):
	return (base + 8, struct.unpack("<d", data[base: base + 8])[0])


ELEMENT_TYPES = {
		0x01 : "double",
		0x02 : "string",
		0x03 : "document",
		0x04 : "array",
		0x05 : "binary",
		0x08 : "boolean",
		0x0A : "none",
		0x10 : "int32",
		0x12 : "int64"
	}

def _encode_double_element(name, value):
	return "\x01" + _encode_cstring(name) + _encode_double(value)

def _decode_double_element(data, base):
	base, name = _decode_cstring(data, base + 1)
	base, value = _decode_double(data, base)
	return (base, name, value)

def _encode_string_element(name, value):
	if isinstance(value, unicode):
		value = value.encode("utf8")
	return "\x02" + _encode_cstring(name) + _encode_string(value)

def _decode_string_element(data, base):
	base, name = _decode_cstring(data, base + 1)
	base, value = _decode_string(data, base)
	value = value.decode("utf8")
	return (base, name, value)

def _encode_document(obj):
	buf = StringIO()
	for name in obj:
		value = obj[name]
		if isinstance(value, float):
			buf.write(_encode_double_element(name, value))
		elif isinstance(value, unicode):
			buf.write(_encode_string_element(name, value))
		elif isinstance(value, dict):
			buf.write(_encode_document_element(name, value))
		elif isinstance(value, list):
			buf.write(_encode_array_element(name, value))
		elif isinstance(value, str):
			buf.write(_encode_binary_element(name, value))
		elif isinstance(value, bool):
			buf.write(_encode_boolean_element(name, value))
		elif value is None:
			buf.write(_encode_none_element(name, value))
		elif isinstance(value, int):
			if value > 0x7ffffff or value < -0x80000000:
				buf.write(_encode_int64_element(name, value))
			else:
				buf.write(_encode_int32_element(name, value))
	e_list = buf.getvalue()
	e_list_length = len(e_list)
	return struct.pack("<i%dsb" % (e_list_length,), e_list_length + 4 + 1,
			e_list, 0)

def _decode_element(data, base):
	element_type = struct.unpack("<b", data[base:base + 1])[0]
	element_description = ELEMENT_TYPES[element_type]
	_decode_func = globals()["_decode_" + element_description + "_element"]
	return _decode_func(data, base)

def _decode_document(data, base):
	length = struct.unpack("<i", data[base:base + 4])[0]
	end_point = base + length
	base += 4
	retval = {}
	while base < end_point - 1:
		base, name, value = _decode_element(data, base)
		retval[name] = value
	return (end_point, retval)

def _encode_document_element(name, value):
	return "\x03" + _encode_cstring(name) + _encode_document(value)

def _decode_document_element(data, base):
	base, name = _decode_cstring(data, base + 1)
	base, value = _decode_document(data, base)
	return (base, name, value)

def _encode_array_element(name, value):
	return "\x04" + _encode_cstring(name) + \
		_encode_document(dict([(str(i), value[i]) for i in xrange(0, len(value))]))

def _decode_array_element(data, base):
	base, name = _decode_cstring(data, base + 1)
	base, value = _decode_document(data, base)
	keys = value.keys()
	keys.sort()
	retval = []
	for i in keys:
		retval.append(value[i])
	return (base, name, retval)

def _encode_binary_element(name, value):
	return "\x05" + _encode_cstring(name) + _encode_binary(value)

def _decode_binary_element(data, base):
	base, name = _decode_cstring(data, base + 1)
	base, value = _decode_binary(data, base)
	return (base, name, value)

def _encode_boolean_element(name, value):
	return "\x08" + _encode_cstring(name) + struct.pack("<b", value)

def _decode_boolean_element(data, base):
	base, name = _decode_cstring(data, base + 1)
	value = not not struct.unpack("<b", data[base:base + 1])[0]
	return (base + 1, name, value)

def _encode_none_element(name, value):
	return "\x0a" + _encode_cstring(name)

def _decode_none_element(data, base):
	base, name = _decode_cstring(data, base + 1)
	return (base, name, None)

def _encode_int32_element(name, value):
	return "\x10" + _encode_cstring(name) + struct.pack("<i", value)

def _decode_int32_element(data, base):
	base, name = _decode_cstring(data, base + 1)
	value = struct.unpack("<i", data[base:base + 4])[0]
	return (base + 4, name, value)

def _encode_int64_element(name, value):
	return "\x12" + _encode_cstring(name) + struct.pack("<Q", value)

def _decode_int64_element(data, base):
	base, name = _decode_cstring(data, base + 1)
	value = struct.unpack("<Q", data[base:base + 8])[0]
	return (base + 8, name, value)
# }}}
# {{{ Public API
def dumps(obj):
	"""
	Given a dict, outputs a BSON string.
	"""
	return _encode_document(obj)

def loads(data):
	"""
	Given a BSON string, outputs a dict.
	"""
	return _decode_document(data, 0)[1]
# }}}
