# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test array transform properties."""

import pytest

from plum.array import ArrayX
from plum.exceptions import SizeError
from plum.littleendian import single, uint8
from plum.str import StrX

ascii_zero = StrX(name="ascii_zero", encoding="ascii", zero_termination=True)


class TestDefault:

    """Test with as many left to default as possible."""

    arrayx = ArrayX(uint8)

    def test_name(self):
        assert self.arrayx.name == "List[int]"

    def test_hint(self):
        assert self.arrayx.__hint__ == "List[int]"

    def test_nbytes(self):
        with pytest.raises(SizeError):
            return self.arrayx.nbytes

    def test_fmt(self):
        assert self.arrayx.fmt is uint8

    def test_dims(self):
        return self.arrayx.dims == (None,)


class TestPositional:

    """Test explicitly defined with positional argument."""

    arrayx = ArrayX(uint8, (2,), "name")

    def test_name(self):
        assert self.arrayx.name == "name"

    def test_hint(self):
        assert self.arrayx.__hint__ == "List[int]"

    def test_nbytes(self):
        assert self.arrayx.nbytes == 2

    def test_fmt(self):
        assert self.arrayx.fmt is uint8

    def test_dims(self):
        return self.arrayx.dims == (2,)


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    arrayx = ArrayX(fmt=uint8, dims=(2,), name="name")


class TestVariable:

    """Test nbytes property when member size is variable."""

    arrayx = ArrayX(name="arrayx", fmt=ascii_zero, dims=(2,))

    def test_nbytes(self):
        with pytest.raises(SizeError):
            return self.arrayx.nbytes


class TestDefaultNameHint:

    """Test generation of name and type hint."""

    def test_multi_dims(self):
        arrayx = ArrayX(fmt=uint8, dims=[20, 30, None])
        assert arrayx.name == arrayx.__hint__ == "List[List[List[int]]]"

    def test_greedy_dim(self):
        arrayx = ArrayX(fmt=single)
        assert arrayx.name == arrayx.__hint__ == "List[float]"

    def test_variable_single_dim(self):
        arrayx = ArrayX(fmt=single, dims=uint8)
        assert arrayx.name == arrayx.__hint__ == "List[float]"

    def test_variable_multi_dim(self):
        dimsx = ArrayX(fmt=uint8, dims=[3])
        arrayx = ArrayX(fmt=single, dims=dimsx)
        assert arrayx.name == arrayx.__hint__ == "List[List[List[float]]]"

    def test_name_override(self):
        arrayx = ArrayX(fmt=single, name="array")
        assert arrayx.__hint__ == "List[float]"
        assert arrayx.name == "array"
