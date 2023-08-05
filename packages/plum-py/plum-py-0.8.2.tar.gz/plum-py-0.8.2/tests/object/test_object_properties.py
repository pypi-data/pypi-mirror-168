# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test IPv4AddressX transform properties."""

from plum.object import ObjectX


def pack(value) -> bytes:
    # pylint: disable=unused-argument
    return b""


def unpack(buffer: bytes) -> bytes:
    # pylint: disable=unused-argument
    return b""


class TestDefault:

    """Test explicitly defined with positional argument."""

    xform = ObjectX(pack, unpack, 1)

    def test_hint(self):
        assert self.xform.__hint__ == "Any"

    def test_name(self):
        assert self.xform.name == "object"

    def test_nbytes(self):
        assert self.xform.nbytes == 1


class TestPositional:

    """Test explicitly defined with positional argument."""

    xform = ObjectX(pack, unpack, 1, "name")

    def test_hint(self):
        assert self.xform.__hint__ == "Any"

    def test_name(self):
        assert self.xform.name == "name"

    def test_nbytes(self):
        assert self.xform.nbytes == 1


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    xform = ObjectX(pack=pack, unpack=unpack, nbytes=1, name="name")
