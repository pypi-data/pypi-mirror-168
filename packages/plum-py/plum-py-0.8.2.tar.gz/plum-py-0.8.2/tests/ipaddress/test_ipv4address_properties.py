# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test IPv4AddressX transform properties."""

from plum.ipaddress import IPv4AddressX


class TestDefault:

    """Test explicitly defined with positional argument."""

    ipv4address = IPv4AddressX()

    def test_hint(self):
        assert self.ipv4address.__hint__ == "IPv4Address"

    def test_name(self):
        assert self.ipv4address.name == "IPv4Address"

    def test_byteorder(self):
        assert self.ipv4address.byteorder == "big"

    def test_nbytes(self):
        assert self.ipv4address.nbytes == 4


class TestPositional:

    """Test explicitly defined with positional argument."""

    ipv4address = IPv4AddressX("little", "name")

    def test_hint(self):
        assert self.ipv4address.__hint__ == "IPv4Address"

    def test_name(self):
        assert self.ipv4address.name == "name"

    def test_byteorder(self):
        assert self.ipv4address.byteorder == "little"

    def test_nbytes(self):
        assert self.ipv4address.nbytes == 4


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    ipv4address = IPv4AddressX(byteorder="little", name="name")
