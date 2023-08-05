# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test float transform properties."""

from plum.float import FloatX


class TestDefault:

    """Test with as many left to default as possible."""

    float32 = FloatX(nbytes=4)

    def test_half(self):
        xform = FloatX(nbytes=2)
        assert xform.__hint__ == "float"
        assert xform.name == "half float"
        assert xform.nbytes == 2
        assert xform.byteorder == "little"

    def test_single(self):
        xform = FloatX(nbytes=4)
        assert xform.__hint__ == "float"
        assert xform.name == "single float"
        assert xform.nbytes == 4
        assert xform.byteorder == "little"

    def test_double(self):
        xform = FloatX(nbytes=8)
        assert xform.__hint__ == "float"
        assert xform.name == "double float"
        assert xform.nbytes == 8
        assert xform.byteorder == "little"


class TestPositional:

    """Test explicitly defined with positional argument."""

    float32 = FloatX(4, "big", "name")

    def test_hint(self):
        assert self.float32.__hint__ == "float"

    def test_name(self):
        assert self.float32.name == "name"

    def test_nbytes(self):
        assert self.float32.nbytes == 4

    def test_byteorder(self):
        assert self.float32.byteorder == "big"


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    float32 = FloatX(nbytes=4, byteorder="big", name="name")
