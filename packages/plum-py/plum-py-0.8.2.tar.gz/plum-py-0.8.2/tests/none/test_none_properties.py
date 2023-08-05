# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test NoneX transform properties."""

from plum.none import NoneX


class TestDefault:

    nonex = NoneX()

    def test_hint(self):
        assert self.nonex.__hint__ == "None"

    def test_name(self):
        assert self.nonex.name == "None"

    def test_nbytes(self):
        assert self.nonex.nbytes == 0


class TestPositional:

    """Test explicitly defined with positional argument."""

    nonex = NoneX("name")

    def test_hint(self):
        assert self.nonex.__hint__ == "None"

    def test_name(self):
        assert self.nonex.name == "name"

    def test_nbytes(self):
        assert self.nonex.nbytes == 0


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    nonex = NoneX(name="name")
