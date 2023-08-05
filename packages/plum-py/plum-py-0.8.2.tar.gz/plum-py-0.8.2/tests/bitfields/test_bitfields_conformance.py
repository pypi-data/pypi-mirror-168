# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test bit fields data store transform API conformance."""

# pylint: disable=unexpected-keyword-arg

from baseline import Baseline

from plum.conformance import Case, CaseData

from sample_bitfields import MyBits, Register


class TestConformance(Case):

    """Test bit fields data store transform conformance."""

    data = CaseData(
        fmt=MyBits,
        bindata=b"\x00\x12",
        nbytes=2,
        values=(
            MyBits(f1=0, f2=Register.R0, f3=True, f4=Register.PC),
            0x1200,
            dict(f1=0, f2=Register.R0, f3=True, f4=Register.PC),
        ),
        dump=Baseline(
            """
            +----------+--------+-------------+-------------------+--------------------+
            | Offset   | Access | Value       | Bytes             | Format             |
            +----------+--------+-------------+-------------------+--------------------+
            | 0        |        | 4608        | 00 12             | MyBits (BitFields) |
            |  [0:8]   | f1     | 0           | ........ 00000000 | int                |
            |  [8:12]  | f2     | Register.R0 | ....0010 ........ | Register           |
            |  [12]    | f3     | True        | ...1.... ........ | bool               |
            |  [13:15] | f4     | Register.PC | .00..... ........ | Register (IntEnum) |
            +----------+--------+-------------+-------------------+--------------------+
            """
        ),
        excess=Baseline(
            """
            +----------+--------+----------------+-------------------+--------------------+
            | Offset   | Access | Value          | Bytes             | Format             |
            +----------+--------+----------------+-------------------+--------------------+
            | 0        |        | 4608           | 00 12             | MyBits (BitFields) |
            |  [0:8]   | f1     | 0              | ........ 00000000 | int                |
            |  [8:12]  | f2     | Register.R0    | ....0010 ........ | Register           |
            |  [12]    | f3     | True           | ...1.... ........ | bool               |
            |  [13:15] | f4     | Register.PC    | .00..... ........ | Register (IntEnum) |
            +----------+--------+----------------+-------------------+--------------------+
            | 2        |        | <excess bytes> | 99                |                    |
            +----------+--------+----------------+-------------------+--------------------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------------------+-------+--------------------+
            | Offset | Value                | Bytes | Format             |
            +--------+----------------------+-------+--------------------+
            | 0      | <insufficient bytes> | 00    | MyBits (BitFields) |
            +--------+----------------------+-------+--------------------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack MyBits (BitFields), 2 needed, only 1
            available
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, f1: int = 171, f2: 'Register', f3: bool, f4: Union[int, 'Register']) -> None:
                self.__value__ = 171
                self.f1 = f1
                self.f2 = f2
                self.f3 = f3
                self.f4 = f4

            @f1.getter
            def f1(self) -> int:
                return int(self) & 255

            @f1.setter
            def f1(self, value: int) -> None:
                value = int(value)
                if not (0 <= value <= 255):
                    raise ValueError("bit field 'f1' requires 0 <= number <= 255")
                self.__value__ = (self.__value__ & -256) | (value & 255)

            @f2.getter
            def f2(self, _typ=f2.typ) -> 'Register':
                return _typ((int(self) >> 8) & 15)

            @f2.setter
            def f2(self, value: 'Register', _typ=f2.typ) -> None:
                value = int(_typ(value))
                self.__value__ = (self.__value__ & -3841) | ((value & 15) << 8)

            @f3.getter
            def f3(self) -> bool:
                return bool((int(self) >> 12) & 1)

            @f3.setter
            def f3(self, value: bool) -> None:
                value = int(bool(value))
                self.__value__ = (self.__value__ & -4097) | ((value & 1) << 12)

            @f4.getter
            def f4(self, _typ=f4.typ) -> Union[int, 'Register']:
                return _typ((int(self) >> 13) & 3)

            @f4.setter
            def f4(self, value: Union[int, 'Register'], _typ=f4.typ) -> None:
                value = int(_typ(value))
                if not (0 <= value <= 3):
                    raise ValueError("bit field 'f4' requires 0 <= number <= 3")
                self.__value__ = (self.__value__ & -24577) | ((value & 3) << 13)

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(f1={self.f1!r}, f2={str(self.f2)}, f3={self.f3!r}, f4={self.f4!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )
