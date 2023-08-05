# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test bytes transform properties."""

from plum.bytes import BytesX


class TestDefault:

    """Test with as many left to default as possible."""

    bytesx = BytesX(name="bytesx", nbytes=4)

    def test_name(self):
        assert self.bytesx.name == "bytesx"

    def test_nbytes(self):
        assert self.bytesx.nbytes == 4

    def test_pad(self):
        assert self.bytesx.pad == b""


class TestPositional:

    """Test explicitly defined with positional argument."""

    bytesx = BytesX(4, b"\x99", "name")

    def test_hint(self):
        assert self.bytesx.__hint__ == "bytes"

    def test_name(self):
        assert self.bytesx.name == "name"

    def test_nbytes(self):
        assert self.bytesx.nbytes == 4

    def test_pad(self):
        assert self.bytesx.pad == b"\x99"


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    bytesx = BytesX(nbytes=4, pad=b"\x99", name="name")


class TestDefaultNameHint:
    def test_greedy(self):
        xform = BytesX()
        assert xform.__hint__ == "bytes"
        assert xform.name == "bytes (greedy)"

    def test_fixed(self):
        xform = BytesX(nbytes=4)
        assert xform.__hint__ == "bytes"
        assert xform.name == "bytes (fixed)"

    def test_padded(self):
        xform = BytesX(nbytes=4, pad=b" ")
        assert xform.__hint__ == "bytes"
        assert xform.name == "bytes (fixed,padded)"
