#!/usr/bin/python -OOOO
# vim: set fileencoding=utf8 shiftwidth=4 tabstop=4 textwidth=80 foldmethod=marker :
# Copyright (c) 2010, Kou Man Tong. All rights reserved.
# For licensing, see LICENSE file included in the package.
"""
BSON serialization and deserialization logic.
Specifications taken from: http://bsonspec.org/#/specification
The following types are unsupported, because for data exchange purposes, they're
over-engineered:
	0x06 (Undefined)
	0x07 (ObjectId)
	0x0b (Regex - Exactly which flavor do you want? Better let higher level
		programmers make that decision.)
	0x0c (DBPointer)
	0x0d (JavaScript code)
	0x0e (Symbol)
	0x0f (JS w/ scope)
	0x11 (MongoDB-specific timestamp)

For binaries, only the default 0x0 type is supported.
"""

from codec import *
__all__ = ["loads", "dumps"]

# {{{ Public API
def dumps(obj):
	"""
	Given a dict, outputs a BSON string.
	"""
	return encode_document(obj)

def loads(data):
	"""
	Given a BSON string, outputs a dict.
	"""
	return decode_document(data, 0)[1]
# }}}
