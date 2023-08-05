"""Test decimal transform exceptions."""

# pylint: disable=unidiomatic-typecheck
import pytest

from baseline import Baseline

from plum.decimal import DecimalX
from plum.conformance import wrap_message
from plum.exceptions import PackError
from plum.utilities import pack


class TestPack:

    """Test pack transform exceptions."""

    def test_cannot_convert(self):
        """Test exception when converting to decimal."""
        with pytest.raises(PackError) as trap:
            pack("foo", DecimalX(2, 1, "big", signed=False, name="u16p1"))

        expected = Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            |        |       |       | u16p1  |
            +--------+-------+-------+--------+

            ValueError occurred during pack operation:

            Value 'foo' cannot be converted to decimal.
            """
        )

        assert wrap_message(trap.value) == expected
