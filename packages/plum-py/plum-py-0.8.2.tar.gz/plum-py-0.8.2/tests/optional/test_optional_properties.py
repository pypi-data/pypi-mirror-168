# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2022 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test OptionalX transform properties."""

import pytest
from plum.exceptions import SizeError
from plum.littleendian import uint8
from plum.optional import OptionalX
from plum.structure import Structure, member


class Sample(Structure):

    member1: int = member(fmt=uint8)


class TestDefaultTransform:

    optional_x = OptionalX(fmt=uint8)

    def test_hint(self):
        assert self.optional_x.__hint__ == "Optional[int]"

    def test_name(self):
        assert self.optional_x.name == "Optional[uint8]"

    def test_fmt(self):
        assert self.optional_x.fmt is uint8

    def test_nbytes(self):
        with pytest.raises(SizeError):
            self.optional_x.nbytes  # pylint: disable=pointless-statement


class TestDefaultTransformClass:

    optional_x = OptionalX(fmt=Sample)

    def test_hint(self):
        assert self.optional_x.__hint__ == "Optional[Sample]"

    def test_name(self):
        assert self.optional_x.name == "Optional[Sample (Structure)]"

    def test_fmt(self):
        assert self.optional_x.fmt is Sample

    def test_nbytes(self):
        with pytest.raises(SizeError):
            self.optional_x.nbytes  # pylint: disable=pointless-statement


class TestPosition:

    optional_x = OptionalX(Sample, "name")

    def test_hint(self):
        assert self.optional_x.__hint__ == "Optional[Sample]"

    def test_name(self):
        assert self.optional_x.name == "name"

    def test_fmt(self):
        assert self.optional_x.fmt is Sample

    def test_nbytes(self):
        with pytest.raises(SizeError):
            self.optional_x.nbytes  # pylint: disable=pointless-statement


class TestKeyword(TestPosition):

    optional_x = OptionalX(fmt=Sample, name="name")
