# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test items transform with fmt=None and nested structure."""

from baseline import Baseline
from plum.items import items
from plum.littleendian import uint8


class Test:

    expected_dump = Baseline(
        """
        +--------+----------+-------+-------+------------+
        | Offset | Access   | Value | Bytes | Format     |
        +--------+----------+-------+-------+------------+
        |        |          |       |       | items:dict |
        |        | ['mbr1'] |       |       | list       |
        | 0      |   [0]    | 1     | 01    | uint8      |
        | 1      |   [1]    | 2     | 02    | uint8      |
        | 2      | ['mbr2'] | 3     | 03    | uint8      |
        +--------+----------+-------+-------+------------+
        """
    )

    expected_bytes = bytes.fromhex("010203")

    sample = dict(mbr1=[(1, uint8), (2, uint8)], mbr2=(3, uint8))

    def test_pack(self):
        assert items.pack(self.sample) == self.expected_bytes

    def test_pack_and_dump(self):
        memory, dump = items.pack_and_dump(self.sample)

        assert memory == self.expected_bytes
        assert str(dump) == self.expected_dump
