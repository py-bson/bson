#!/usr/bin/python -OOOO
# vim: set fileencoding=utf8 shiftwidth=4 tabstop=4 textwidth=80 foldmethod=marker :
# Copyright (c) 2010, Kou Man Tong. All rights reserved.
# Copyright (c) 2015, Ayun Park. All rights reserved.
# For licensing, see LICENSE file included in the package.
"""
Base codec functions for bson.
"""
import struct
import warnings
from datetime import datetime
from abc import ABCMeta, abstractmethod
try:
    from io import BytesIO as StringIO
except ImportError:
    from cStringIO import StringIO

import calendar
import pytz
from binascii import b2a_hex

from six import integer_types, iterkeys, text_type, PY3
from six.moves import xrange


class MissingClassDefinition(ValueError):
    def __init__(self, class_name):
        super(MissingClassDefinition, self).__init__("No class definition for class %s" % (class_name,))


class UnknownSerializerError(ValueError):
    pass


class MissingTimezoneWarning(RuntimeWarning):
    def __init__(self, *args):
        args = list(args)
        if len(args) < 1:
            args.append("Input datetime object has no tzinfo, assuming UTC.")
        super(MissingTimezoneWarning, self).__init__(*args)


class TraversalStep(object):
    def __init__(self, parent, key):
        self.parent = parent
        self.key = key


class BSONCoding(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def bson_encode(self):
       pass

    @abstractmethod
    def bson_init(self, raw_values):
        pass


classes = {}


def import_class(cls):
    if not issubclass(cls, BSONCoding):
        return

    global classes
    classes[cls.__name__] = cls


def import_classes(*args):
    for cls in args:
       import_class(cls)


def import_classes_from_modules(*args):
    for module in args:
        for item in module.__dict__:
            if hasattr(item, "__new__") and hasattr(item, "__name__"):
                import_class(item)


def encode_object(obj, traversal_stack, generator_func, on_unknown=None):
    values = obj.bson_encode()
    class_name = obj.__class__.__name__
    values["$$__CLASS_NAME__$$"] = class_name
    return encode_document(values, traversal_stack, obj, generator_func, on_unknown)


def encode_object_element(name, value, traversal_stack, generator_func, on_unknown):
    return b"\x03" + encode_cstring(name) + encode_object(value, traversal_stack, generator_func=generator_func, on_unknown=on_unknown)


class _EmptyClass(object):
    pass


def decode_object(raw_values):
    global classes
    class_name = raw_values["$$__CLASS_NAME__$$"]
    cls = None
    try:
        cls = classes[class_name]
    except KeyError:
        raise MissingClassDefinition(class_name)

    retval = _EmptyClass()
    retval.__class__ = cls
    alt_retval = retval.bson_init(raw_values)
    return alt_retval or retval


def encode_string(value):
    value = value.encode("utf-8")
    length = len(value)
    return struct.pack("<i%dsb" % (length,), length + 1, value, 0)


def decode_string(data, base):
    length = struct.unpack("<i", data[base:base + 4])[0]
    value = data[base + 4: base + 4 + length - 1]
    value = value.decode("utf-8")
    return base + 4 + length, value


def encode_cstring(value):
    if "\x00" in value:
        raise ValueError("Element names may not include NUL bytes.")
        # A NUL byte is used to delimit our string, accepting one would cause
        # our string to terminate early.
    if isinstance(value, integer_types):
        value = str(value)
    if isinstance(value, text_type):
        value = value.encode("utf-8")
    return value + b"\x00"


def decode_cstring(data, base):
    length = 0
    max_length = len(data) - base
    while length < max_length:
        character = data[base + length]
        if PY3:
            character = chr(character)
        length += 1
        if character == "\x00":
            break
    return base + length, data[base:base + length - 1].decode("utf-8")


def encode_binary(value):
    length = len(value)
    return struct.pack("<ib", length, 0) + value


def decode_binary(data, base):
    length, binary_type = struct.unpack("<ib", data[base:base + 5])
    return base + 5 + length, data[base + 5:base + 5 + length]


def encode_double(value):
    return struct.pack("<d", value)


def decode_double(data, base):
    return base + 8, struct.unpack("<d", data[base: base + 8])[0]


ELEMENT_TYPES = {
    0x01: "double",
    0x02: "string",
    0x03: "document",
    0x04: "array",
    0x05: "binary",
    0x07: "object_id",
    0x08: "boolean",
    0x09: "UTCdatetime",
    0x0A: "none",
    0x10: "int32",
    0x12: "int64"
}


def encode_double_element(name, value):
    return b"\x01" + encode_cstring(name) + encode_double(value)


def decode_double_element(data, base):
    base, name = decode_cstring(data, base + 1)
    base, value = decode_double(data, base)
    return base, name, value


def encode_string_element(name, value):
    return b"\x02" + encode_cstring(name) + encode_string(value)


def decode_string_element(data, base):
    base, name = decode_cstring(data, base + 1)
    base, value = decode_string(data, base)
    return base, name, value


def encode_value(name, value, buf, traversal_stack, generator_func, on_unknown=None):
    if isinstance(value, BSONCoding):
        buf.write(encode_object_element(name, value, traversal_stack, generator_func, on_unknown))
    elif isinstance(value, float):
        buf.write(encode_double_element(name, value))
    elif isinstance(value, text_type):
        buf.write(encode_string_element(name, value))
    elif isinstance(value, dict):
        buf.write(encode_document_element(name, value, traversal_stack, generator_func, on_unknown))
    elif isinstance(value, list) or isinstance(value, tuple):
        buf.write(encode_array_element(name, value, traversal_stack, generator_func, on_unknown))
    elif isinstance(value, str) or isinstance(value, bytes):
        buf.write(encode_binary_element(name, value))
    elif isinstance(value, bool):
        buf.write(encode_boolean_element(name, value))
    elif isinstance(value, datetime):
        buf.write(encode_UTCdatetime_element(name, value))
    elif value is None:
        buf.write(encode_none_element(name, value))
    elif isinstance(value, integer_types):
        if not PY3 and isinstance(value, long):
            buf.write(encode_int64_element(name, value))
        else:
            if value < -0x80000000 or value > 0x7fffffff:
                buf.write(encode_int64_element(name, value))
            else:
                buf.write(encode_int32_element(name, value))
    else:
        if on_unknown is not None:
            encode_value(name, on_unknown(value), buf, traversal_stack, generator_func, on_unknown)
        else:
            raise UnknownSerializerError()


def encode_document(obj, traversal_stack, traversal_parent=None, generator_func=None, on_unknown=None):
    buf = StringIO()
    key_iter = iterkeys(obj)
    if generator_func is not None:
        key_iter = generator_func(obj, traversal_stack)
    for name in key_iter:
        value = obj[name]
        traversal_stack.append(TraversalStep(traversal_parent or obj, name))
        encode_value(name, value, buf, traversal_stack, generator_func, on_unknown)
        traversal_stack.pop()
    e_list = buf.getvalue()
    e_list_length = len(e_list)
    return struct.pack("<i%dsb" % (e_list_length,), e_list_length + 4 + 1, e_list, 0)


def encode_array(array, traversal_stack, traversal_parent = None, generator_func = None, on_unknown = None):
    buf = StringIO()
    for i in xrange(0, len(array)):
        value = array[i]
        traversal_stack.append(TraversalStep(traversal_parent or array, i))
        encode_value(text_type(i), value, buf, traversal_stack, generator_func, on_unknown)
        traversal_stack.pop()
    e_list = buf.getvalue()
    e_list_length = len(e_list)
    return struct.pack("<i%dsb" % (e_list_length,), e_list_length + 4 + 1, e_list, 0)


def decode_element(data, base):
    element_type = struct.unpack("<b", data[base:base + 1])[0]
    element_description = ELEMENT_TYPES[element_type]
    decode_func = globals()["decode_" + element_description + "_element"]
    return decode_func(data, base)


def decode_document(data, base):
    length = struct.unpack("<i", data[base:base + 4])[0]
    end_point = base + length
    if data[end_point - 1] not in ('\0', 0):
        raise ValueError('missing null-terminator in document')
    base += 4
    retval = {}
    while base < end_point - 1:
        base, name, value = decode_element(data, base)
        retval[name] = value
    if "$$__CLASS_NAME__$$" in retval:
        retval = decode_object(retval)
    return end_point, retval


def encode_document_element(name, value, traversal_stack, generator_func, on_unknown):
    return b"\x03" + encode_cstring(name) + encode_document(value, traversal_stack, generator_func=generator_func, on_unknown=on_unknown)


def decode_document_element(data, base):
    base, name = decode_cstring(data, base + 1)
    base, value = decode_document(data, base)
    return base, name, value


def encode_array_element(name, value, traversal_stack, generator_func, on_unknown):
    return b"\x04" + encode_cstring(name) + encode_array(value, traversal_stack, generator_func=generator_func, on_unknown=on_unknown)


def decode_array_element(data, base):
    base, name = decode_cstring(data, base + 1)
    base, value = decode_document(data, base)
    retval = []
    try:
        i = 0
        while True:
            retval.append(value[text_type(i)])
            i += 1
    except KeyError:
        pass
    return base, name, retval


def encode_binary_element(name, value):
    return b"\x05" + encode_cstring(name) + encode_binary(value)


def decode_binary_element(data, base):
    base, name = decode_cstring(data, base + 1)
    base, value = decode_binary(data, base)
    return base, name, value


def encode_boolean_element(name, value):
    return b"\x08" + encode_cstring(name) + struct.pack("<b", value)


def decode_boolean_element(data, base):
    base, name = decode_cstring(data, base + 1)
    value = not not struct.unpack("<b", data[base:base + 1])[0]
    return base + 1, name, value


def encode_UTCdatetime_element(name, value):
    if value.tzinfo is None:
        warnings.warn(MissingTimezoneWarning(), None, 4)
    value = int(round(calendar.timegm(value.utctimetuple()) * 1000 + (value.microsecond / 1000.0)))
    return b"\x09" + encode_cstring(name) + struct.pack("<q", value)


def decode_UTCdatetime_element(data, base):
    base, name = decode_cstring(data, base + 1)
    value = datetime.fromtimestamp(struct.unpack("<q", data[base:base + 8])[0] / 1000.0, pytz.utc)
    return base + 8, name, value


def encode_none_element(name, value):
    return b"\x0a" + encode_cstring(name)


def decode_none_element(data, base):
    base, name = decode_cstring(data, base + 1)
    return base, name, None


def encode_int32_element(name, value):
    value = struct.pack("<i", value)
    return b"\x10" + encode_cstring(name) + value


def decode_int32_element(data, base):
    base, name = decode_cstring(data, base + 1)
    value = struct.unpack("<i", data[base:base + 4])[0]
    return base + 4, name, value


def encode_int64_element(name, value):
    return b"\x12" + encode_cstring(name) + struct.pack("<q", value)


def decode_int64_element(data, base):
    base, name = decode_cstring(data, base + 1)
    value = struct.unpack("<q", data[base:base + 8])[0]
    return base + 8, name, value


def encode_object_id_element(name, value):
    return b"\x07" + encode_cstring(name) + value


def decode_object_id_element(data, base):
    base, name = decode_cstring(data, base + 1)
    value = b2a_hex(data[base:base + 12])
    return base + 12, name, value
