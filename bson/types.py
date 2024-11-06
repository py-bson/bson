class Int32:
    """A signed integer with a 32-bit fixed width."""

    def __init__(self, value):
        if value < -(2**31) or value > 2**31 - 1:
            raise ValueError(f"{value} cannot be represented in int32")
        self._value = value

    def get_value(self):
        return self._value

    def __str__(self):
        return str(self._value)


class Int64:
    """A signed integer with a 64-bit fixed width."""

    def __init__(self, value):
        if value < -(2**63) or value > 2**63 - 1:
            raise ValueError(f"{value} cannot be represented in int64")
        self._value = value

    def get_value(self):
        return self._value

    def __str__(self):
        return str(self._value)


class UInt64:
    """An unsigned integer with a 64-bit fixed width."""

    def __init__(self, value):
        if value < 0 or value > 2**64 - 1:
            raise ValueError(f"{value} cannot be represented in uint64")
        self._value = value

    def get_value(self):
        return self._value

    def __str__(self):
        return str(self._value)
