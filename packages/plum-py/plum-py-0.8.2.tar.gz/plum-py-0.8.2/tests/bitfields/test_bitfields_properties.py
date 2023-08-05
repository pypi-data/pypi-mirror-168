# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test BitFields data store transform properties."""
# pylint: disable=comparison-with-callable

from typing import Union
from enum import IntEnum

from plum.bitfields import BitFields, bitfield
from plum.enum import EnumX


class TestDefault:

    """Test with as many left to default as possible."""

    class Sample(BitFields):

        """Sample bit fields data store transform type."""

        m0: int = bitfield(size=1)
        m1: int = bitfield(size=1)

    def test_nbytes(self):
        assert self.Sample.nbytes == 1
        assert self.Sample.from_int(0).nbytes == 1

    def test_byteorder(self):
        assert self.Sample.byteorder == "little"

    def test_default(self):
        assert self.Sample.default == 0

    def test_ignore(self):
        assert self.Sample.ignore == 0

    def test_nested(self):
        assert self.Sample.nested is False


class TestKeyword:

    """Test explicitly defined with keyword argument."""

    class Sample(
        BitFields, nbytes=2, byteorder="big", default=1, ignore=2, nested=True
    ):

        """Sample bit fields data store transform type."""

        m0: int = bitfield(size=1)
        m1: int = bitfield(size=1)

    def test_nbytes(self):
        assert self.Sample.nbytes == 2
        assert self.Sample.from_int(0).nbytes == 2

    def test_byteorder(self):
        assert self.Sample.byteorder == "big"

    def test_default(self):
        assert self.Sample.default == 1

    def test_ignore(self):
        assert self.Sample.ignore == 2

    def test_nested(self):
        assert self.Sample.nested is True


class TestNameAndHint:
    class Sample(BitFields):

        m0: int = bitfield(size=1)
        m1: int = bitfield(size=1)

    def test_name(self):
        assert self.Sample.name == "Sample (BitFields)"
        assert self.Sample.__name__ == "Sample"

    def test_hint(self):
        assert self.Sample.__hint__ == "Sample"
        assert self.Sample.__hint__ == "Sample"


class Bits(IntEnum):

    ZEROES = 0x00
    ONES = 0x03


class TestBitFieldAccess:
    class Sample(BitFields):

        number: int = bitfield(size=3, lsb=0)
        boolean: int = bitfield(size=1, lsb=3, typ=bool)
        enumeration: Bits = bitfield(size=2, lsb=4, typ=Bits)
        enumeration_transform: Union[Bits, int] = bitfield(
            size=2, lsb=6, typ=EnumX(enum=Bits, strict=False)
        )

    def test_get(self):
        assert self.Sample.from_int(0xF8).number == 0
        assert self.Sample.from_int(0x07).number == 7

        assert self.Sample.from_int(0xF7).boolean is False
        assert self.Sample.from_int(0x08).boolean is True

        assert self.Sample.from_int(0xCF).enumeration is Bits.ZEROES
        assert self.Sample.from_int(0x30).enumeration is Bits.ONES

        assert self.Sample.from_int(0x3F).enumeration_transform is Bits.ZEROES
        assert self.Sample.from_int(0xC0).enumeration_transform is Bits.ONES

    def test_set(self):
        sample = self.Sample.from_int(0)
        sample.number = 7
        assert int(sample) == 0x07

        sample = self.Sample.from_int(0)
        sample.boolean = True
        assert int(sample) == 0x08

        sample = self.Sample.from_int(0)
        sample.enumeration = Bits.ONES
        assert int(sample) == 0x30

        sample = self.Sample.from_int(0)
        sample.enumeration_transform = Bits.ONES
        assert int(sample) == 0xC0
