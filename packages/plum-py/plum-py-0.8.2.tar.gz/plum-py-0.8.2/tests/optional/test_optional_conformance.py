# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2022 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test NoneX transform API conformance."""

from baseline import Baseline

from plum.conformance import Case, CaseData
from plum.littleendian import uint8
from plum.optional import OptionalX

optional_x = OptionalX(fmt=uint8)


class TestMissing(Case):

    data = CaseData(
        fmt=OptionalX(fmt=uint8),
        bindata=b"",
        nbytes=None,
        values=(None,),
        dump=Baseline(
            """
            +--------+-------+-------+-----------------+
            | Offset | Value | Bytes | Format          |
            +--------+-------+-------+-----------------+
            |        | None  |       | Optional[uint8] |
            +--------+-------+-------+-----------------+
            """
        ),
        excess="N/A",
        shortage="N/A",
    )


class TestPresent(Case):

    data = CaseData(
        fmt=OptionalX(fmt=uint8),
        bindata=bytes.fromhex("12"),
        nbytes=None,
        values=(0x12,),
        dump=Baseline(
            """
            +--------+-------+-------+-----------------+
            | Offset | Value | Bytes | Format          |
            +--------+-------+-------+-----------------+
            | 0      | 18    | 12    | Optional[uint8] |
            +--------+-------+-------+-----------------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------------+-------+-----------------+
            | Offset | Value          | Bytes | Format          |
            +--------+----------------+-------+-----------------+
            | 0      | 18             | 12    | Optional[uint8] |
            +--------+----------------+-------+-----------------+
            | 1      | <excess bytes> | 99    |                 |
            +--------+----------------+-------+-----------------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage="N/A",
    )
