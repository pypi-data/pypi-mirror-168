# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test miscellaneous features of AttrDict and AttrDictX transform."""

import pytest

from baseline import Baseline

from plum.attrdict import AttrDict, AttrDictX
from plum.array import ArrayX
from plum.conformance import wrap_message
from plum.exceptions import SizeError
from plum.littleendian import uint8, uint16


class TestAttrDictX:

    """Test AttrDictX features."""

    def test_default_name(self):
        xform = AttrDictX(dict(m1=uint8, m2=uint16))
        assert xform.name == "AttrDict"

    def test_explicit_name(self):
        xform = AttrDictX(dict(m1=uint8, m2=uint16), name="name")
        assert xform.name == "name"

    def test_default_hint(self):
        xform = AttrDictX(dict(m1=uint8, m2=uint16))
        assert xform.__hint__ == "AttrDict"

    def test_size_error(self):
        """Verify no size when a member has no size."""
        expected_message = Baseline(
            """
            <transform 'AttrDict'> sizes vary
            """
        )

        xform = AttrDictX({"m1": ArrayX(name="list", fmt=uint8), "m2": uint8})

        with pytest.raises(SizeError) as trap:
            xform.nbytes  # pylint: disable=pointless-statement

        assert wrap_message(trap.value) == expected_message


class TestAttrDict:

    """Test AttrDict properties."""

    def test_attribute_access(self):
        dct = AttrDict(m1=1)
        assert dct["m1"] == 1
        assert dct.m1 == 1  # pylint: disable=no-member

    def test_repr(self):
        expected_repr = Baseline(
            """
            AttrDict(m1=1, m2=2)
            """
        )

        assert repr(AttrDict(m1=1, m2=2)) == expected_repr


class TestEmptyValueInDump:

    xform = AttrDictX({})

    expected_dump = Baseline(
        """
        +--------+-------+-------+----------+
        | Offset | Value | Bytes | Format   |
        +--------+-------+-------+----------+
        |        | {}    |       | AttrDict |
        +--------+-------+-------+----------+
        """
    )

    def test_pack(self):
        buffer, dump = self.xform.pack_and_dump({})
        assert buffer == b""
        assert str(dump) == self.expected_dump

    def test_unpack(self):
        value, dump = self.xform.unpack_and_dump(b"")
        assert value == {}
        assert str(dump) == self.expected_dump
