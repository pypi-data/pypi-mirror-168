# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2022 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test miscellaneous array transform features."""

from baseline import Baseline
from plum.array import ArrayX
from plum.littleendian import uint8


class TestDumpWhenArrayEmpty:

    array_x = ArrayX(name="list", fmt=uint8)

    expected_dump = Baseline(
        """
        +--------+-------+-------+--------+
        | Offset | Value | Bytes | Format |
        +--------+-------+-------+--------+
        |        | []    |       | list   |
        +--------+-------+-------+--------+
        """
    )

    def test_pack(self):
        _, dump = self.array_x.pack_and_dump([])
        assert str(dump) == self.expected_dump

    def test_unpack(self):
        _, dump = self.array_x.unpack_and_dump(b"")
        assert str(dump) == self.expected_dump
