# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test items transform properties."""

import pytest

from plum.exceptions import SizeError
from plum.items import ItemsX
from plum.littleendian import uint8


class TestDefault:

    """Test with as many left to default as possible."""

    itemsx = ItemsX()

    def test_name(self):
        assert self.itemsx.name == "Any"

    def test_hint(self):
        assert self.itemsx.name == "Any"

    def test_nbytes(self):
        with pytest.raises(SizeError):
            return self.itemsx.nbytes

    def test_fmt(self):
        assert self.itemsx.fmt is None


class TestPositional:

    """Test explicitly defined with positional argument."""

    itemsx = ItemsX(uint8, "name")

    def test_hint(self):
        assert self.itemsx.__hint__ == "int"

    def test_name(self):
        assert self.itemsx.name == "name"

    def test_nbytes(self):
        assert self.itemsx.nbytes == 1

    def test_fmt(self):
        assert self.itemsx.fmt is uint8


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    itemsx = ItemsX(fmt=uint8, name="name")


class TestDefaultNameHint:
    def test_none(self):
        xform = ItemsX(fmt=None)
        assert xform.name == xform.__hint__ == "Any"

    def test_tuple(self):
        xform = ItemsX(fmt=(None, uint8))
        assert xform.name == xform.__hint__ == "Tuple[Any, int]"

    def test_list_uniform(self):
        xform = ItemsX(fmt=[uint8, uint8])
        assert xform.name == xform.__hint__ == "List[int]"

    def test_list_varied(self):
        xform = ItemsX(fmt=[uint8, None])
        assert xform.name == xform.__hint__ == "List[Any]"

    def test_dict_uniform(self):
        xform = ItemsX(fmt={"a": uint8, "b": uint8})
        assert xform.name == xform.__hint__ == "Dict[str, int]"

    def test_dict_varied(self):
        xform = ItemsX(fmt={"a": uint8, "b": None})
        assert xform.name == xform.__hint__ == "Dict[str, Any]"

    def test_nested(self):
        xform = ItemsX(fmt=((None, uint8), {"a": uint8}))
        assert xform.name == xform.__hint__ == "Tuple[Tuple[Any, int], Dict[str, int]]"
