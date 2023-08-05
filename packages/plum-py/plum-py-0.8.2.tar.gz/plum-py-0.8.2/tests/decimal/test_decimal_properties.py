"""Test decimal transform properties."""

from plum.decimal import DecimalX


class TestProperties:

    """Test with as many left to default as possible."""

    u16p1 = DecimalX(2, 1, "big", signed=False, name="u16p1")

    def test_hint(self):
        assert self.u16p1.__hint__ == "Decimal"

    def test_name(self):
        assert self.u16p1.name == "u16p1"

    def test_nbytes(self):
        assert self.u16p1.nbytes == 2

    def test_byteorder(self):
        assert self.u16p1.byteorder == "big"

    def test_signed(self):
        assert self.u16p1.signed is False

    def test_precision(self):
        assert self.u16p1.precision == 1


class TestDefaultNameAndHint:
    def test_hint(self):
        xform = DecimalX(2, 1)
        assert xform.__hint__ == "Decimal"

    def test_name(self):
        xform = DecimalX(2, 1)
        assert xform.name == "Decimal (precision=1)"
