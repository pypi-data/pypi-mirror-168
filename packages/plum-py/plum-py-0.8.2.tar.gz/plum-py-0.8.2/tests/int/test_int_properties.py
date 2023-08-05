# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer transform properties."""

from plum.int import IntX


class TestDefault:

    """Test with as many left to default as possible."""

    uint8 = IntX(1)

    def test_name(self):
        assert self.uint8.name == "uint8"

    def test_hint(self):
        assert self.uint8.__hint__ == "int"

    def test_nbytes(self):
        assert self.uint8.nbytes == 1

    def test_byteorder(self):
        assert self.uint8.byteorder == "little"

    def test_signed(self):
        assert self.uint8.signed is False


class TestPositional:

    """Test explicitly defined with positional argument."""

    uint8 = IntX(2, "big", signed=True, name="name")

    def test_hint(self):
        assert self.uint8.__hint__ == "int"

    def test_name(self):
        assert self.uint8.name == "name"

    def test_nbytes(self):
        assert self.uint8.nbytes == 2

    def test_byteorder(self):
        assert self.uint8.byteorder == "big"

    def test_signed(self):
        assert self.uint8.signed is True


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    uint8 = IntX(nbytes=2, byteorder="big", signed=True, name="name")


class DefaultNameHint:
    def test_signed(self):
        int_x = IntX(nbytes=2, signed=True)
        assert int_x.name == "sint16"
        assert int_x.__hint__ == "int"

    def test_unsigned(self):
        int_x = IntX(nbytes=2, signed=False)
        assert int_x.name == "uint16"
        assert int_x.__hint__ == "int"

    def test_bigendian(self):
        int_x = IntX(nbytes=2, byteorder="big")
        assert int_x.name == "uint16"
        assert int_x.__hint__ == "int"

    def test_littleendian(self):
        int_x = IntX(nbytes=2, byteorder="little")
        assert int_x.name == "uint16"
        assert int_x.__hint__ == "int"

    def test_nbytes(self):
        int_x = IntX(nbytes=10)
        assert int_x.name == "uint80"
        assert int_x.__hint__ == "int"
