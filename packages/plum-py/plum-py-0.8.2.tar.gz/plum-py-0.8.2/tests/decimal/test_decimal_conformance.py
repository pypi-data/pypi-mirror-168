"""Test int transform API conformance."""

from baseline import Baseline
from decimal import Decimal

from plum.decimal import DecimalX
from plum.conformance import Case, CaseData


class TestU16Precsion1(Case):

    """Test unsigned 16 bit big endian decimal."""

    data = CaseData(
        fmt=DecimalX(2, 1, "big", signed=False, name="u16p1"),
        bindata=b"\x01\x02",
        nbytes=2,
        values=(Decimal("25.8"),),
        dump=Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            | 0      | 25.8  | 01 02 | u16p1  |
            +--------+-------+-------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------------+-------+--------+
            | Offset | Value          | Bytes | Format |
            +--------+----------------+-------+--------+
            | 0      | 25.8           | 01 02 | u16p1  |
            +--------+----------------+-------+--------+
            | 2      | <excess bytes> | 99    |        |
            +--------+----------------+-------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------------------+-------+--------+
            | Offset | Value                | Bytes | Format |
            +--------+----------------------+-------+--------+
            | 0      | <insufficient bytes> | 01    | u16p1  |
            +--------+----------------------+-------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack u16p1, 2 needed, only 1 available
            """
        ),
    )


class TestS16Precsion1(Case):

    """Test signed 16 bit big endian decimal."""

    data = CaseData(
        fmt=DecimalX(2, 1, "big", signed=True, name="s16p1"),
        bindata=b"\xFF\x12",
        nbytes=2,
        values=(Decimal("-23.8"),),
        dump=Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            | 0      | -23.8 | ff 12 | s16p1  |
            +--------+-------+-------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------------+-------+--------+
            | Offset | Value          | Bytes | Format |
            +--------+----------------+-------+--------+
            | 0      | -23.8          | ff 12 | s16p1  |
            +--------+----------------+-------+--------+
            | 2      | <excess bytes> | 99    |        |
            +--------+----------------+-------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------------------+-------+--------+
            | Offset | Value                | Bytes | Format |
            +--------+----------------------+-------+--------+
            | 0      | <insufficient bytes> | ff    | s16p1  |
            +--------+----------------------+-------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack s16p1, 2 needed, only 1 available
            """
        ),
    )


class TestU16Precsion2(Case):

    """Test unsigned 16 bit little endian decimal."""

    data = CaseData(
        fmt=DecimalX(2, 2, "little", signed=False, name="u16p2"),
        bindata=b"\x02\x01",
        nbytes=2,
        values=(Decimal("2.58"),),
        dump=Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            | 0      | 2.58  | 02 01 | u16p2  |
            +--------+-------+-------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------------+-------+--------+
            | Offset | Value          | Bytes | Format |
            +--------+----------------+-------+--------+
            | 0      | 2.58           | 02 01 | u16p2  |
            +--------+----------------+-------+--------+
            | 2      | <excess bytes> | 99    |        |
            +--------+----------------+-------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------------------+-------+--------+
            | Offset | Value                | Bytes | Format |
            +--------+----------------------+-------+--------+
            | 0      | <insufficient bytes> | 02    | u16p2  |
            +--------+----------------------+-------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack u16p2, 2 needed, only 1 available
            """
        ),
    )


class TestU8Precsion0(Case):

    """Test unsigned 8 bit 0 precision decimal."""

    data = CaseData(
        fmt=DecimalX(1, 0, "big", signed=False, name="u8p0"),
        bindata=b"\x01",
        nbytes=1,
        values=(Decimal("1"),),
        dump=Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            | 0      | 1     | 01    | u8p0   |
            +--------+-------+-------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------------+-------+--------+
            | Offset | Value          | Bytes | Format |
            +--------+----------------+-------+--------+
            | 0      | 1              | 01    | u8p0   |
            +--------+----------------+-------+--------+
            | 1      | <excess bytes> | 99    |        |
            +--------+----------------+-------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------------------+-------+--------+
            | Offset | Value                | Bytes | Format |
            +--------+----------------------+-------+--------+
            |        | <insufficient bytes> |       | u8p0   |
            +--------+----------------------+-------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack u8p0, 1 needed, only 0 available
            """
        ),
    )
