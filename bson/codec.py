#!/usr/bin/python -OOOO
# vim: set fileencoding=utf8 shiftwidth=4 tabstop=4 textwidth=80 foldmethod=marker :
# Copyright (c) 2010, Kou Man Tong. All rights reserved.
# For licensing, see LICENSE file included in the package.
"""
Base codec functions for bson.
"""
import struct
try:
	import StringIO as StringIO
except ImportError:
	import StringIO

# {{{ Private Logic
def encode_string(value):
	value = value.encode("utf8")
	length = len(value)
	return struct.pack("<i%dsb" % (length,), length + 1, value, 0)

def decode_string(data, base):
	length = struct.unpack("<i", data[base:base + 4])[0]
	value = data[base + 4: base + 4 + length - 1]
	value = value.decode("utf8")
	return (base + 4 + length, value)

def encode_cstring(value):
	if isinstance(value, unicode):
		value = value.encode("utf8")
	return value + "\x00"

def decode_cstring(data, base):
	buf = StringIO.StringIO()
	length = 0
	for character in data[base:]:
		length += 1
		if character == "\x00":
			break
		buf.write(character)
	return (base + length, buf.getvalue().decode("utf8"))

def encode_binary(value):
	length = len(value)
	return struct.pack("<ib", length, 0) + value

def decode_binary(data, base):
	length, binary_type = struct.unpack("<ib", data[base:base + 5])
	return (base + 5 + length, data[base + 5:base + 5 + length])

def encode_double(value):
	return struct.pack("<d", value)

def decode_double(data, base):
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

def encode_double_element(name, value):
	return "\x01" + encode_cstring(name) + encode_double(value)

def decode_double_element(data, base):
	base, name = decode_cstring(data, base + 1)
	base, value = decode_double(data, base)
	return (base, name, value)

def encode_string_element(name, value):
	return "\x02" + encode_cstring(name) + encode_string(value)

def decode_string_element(data, base):
	base, name = decode_cstring(data, base + 1)
	base, value = decode_string(data, base)
	return (base, name, value)

def encode_document(obj):
	buf = StringIO.StringIO()
	for name in obj:
		value = obj[name]
		if isinstance(value, float):
			buf.write(encode_double_element(name, value))
		elif isinstance(value, unicode):
			buf.write(encode_string_element(name, value))
		elif isinstance(value, dict):
			buf.write(encode_document_element(name, value))
		elif isinstance(value, list) or isinstance(value, tuple):
			buf.write(encode_array_element(name, value))
		elif isinstance(value, str):
			buf.write(encode_binary_element(name, value))
		elif isinstance(value, bool):
			buf.write(encode_boolean_element(name, value))
		elif value is None:
			buf.write(encode_none_element(name, value))
		elif isinstance(value, int):
			buf.write(encode_int32_element(name, value))
		elif isinstance(value, long):
			buf.write(encode_int64_element(name, value))
	e_list = buf.getvalue()
	e_list_length = len(e_list)
	return struct.pack("<i%dsb" % (e_list_length,), e_list_length + 4 + 1,
			e_list, 0)

def decode_element(data, base):
	element_type = struct.unpack("<b", data[base:base + 1])[0]
	element_description = ELEMENT_TYPES[element_type]
	decode_func = globals()["decode_" + element_description + "_element"]
	return decode_func(data, base)

def decode_document(data, base):
	length = struct.unpack("<i", data[base:base + 4])[0]
	end_point = base + length
	base += 4
	retval = {}
	while base < end_point - 1:
		base, name, value = decode_element(data, base)
		retval[name] = value
	return (end_point, retval)

def encode_document_element(name, value):
	return "\x03" + encode_cstring(name) + encode_document(value)

def decode_document_element(data, base):
	base, name = decode_cstring(data, base + 1)
	base, value = decode_document(data, base)
	return (base, name, value)

def encode_array_element(name, value):
	return "\x04" + encode_cstring(name) + \
		encode_document(dict([(str(i), value[i]) for i in xrange(0, len(value))]))

def decode_array_element(data, base):
	base, name = decode_cstring(data, base + 1)
	base, value = decode_document(data, base)
	keys = value.keys()
	keys.sort()
	retval = []
	for i in keys:
		retval.append(value[i])
	return (base, name, retval)

def encode_binary_element(name, value):
	return "\x05" + encode_cstring(name) + encode_binary(value)

def decode_binary_element(data, base):
	base, name = decode_cstring(data, base + 1)
	base, value = decode_binary(data, base)
	return (base, name, value)

def encode_boolean_element(name, value):
	return "\x08" + encode_cstring(name) + struct.pack("<b", value)

def decode_boolean_element(data, base):
	base, name = decode_cstring(data, base + 1)
	value = not not struct.unpack("<b", data[base:base + 1])[0]
	return (base + 1, name, value)

def encode_none_element(name, value):
	return "\x0a" + encode_cstring(name)

def decode_none_element(data, base):
	base, name = decode_cstring(data, base + 1)
	return (base, name, None)

def encode_int32_element(name, value):
	return "\x10" + encode_cstring(name) + struct.pack("<i", value)

def decode_int32_element(data, base):
	base, name = decode_cstring(data, base + 1)
	value = struct.unpack("<i", data[base:base + 4])[0]
	return (base + 4, name, value)

def encode_int64_element(name, value):
	return "\x12" + encode_cstring(name) + struct.pack("<q", value)

def decode_int64_element(data, base):
	base, name = decode_cstring(data, base + 1)
	value = struct.unpack("<q", data[base:base + 8])[0]
	return (base + 8, name, value)
# }}}
