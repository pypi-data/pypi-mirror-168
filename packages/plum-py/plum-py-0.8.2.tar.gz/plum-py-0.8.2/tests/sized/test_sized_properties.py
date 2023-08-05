# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test SizedX transform API conformance."""

from plum.littleendian import uint8
from plum.sized import SizedX
from plum.str import StrX


ascii_greedy = StrX(name="ascii", encoding="ascii")

sized_string = SizedX(
    fmt=ascii_greedy,
    size_fmt=uint8,
    size_access="--nbytes--",
    name="sized_string",
)


class TestDefaults:

    xform = SizedX(fmt=ascii_greedy, size_fmt=uint8)

    def test_fmt(self):
        assert self.xform.fmt is ascii_greedy

    def test_hint(self):
        assert self.xform.__hint__ == "str"

    def test_name(self):
        assert self.xform.name == "sized: str"

    def test_offset(self):
        assert self.xform.offset == 0

    def test_ratio(self):
        assert self.xform.ratio == 1

    def test_size_access(self):
        assert self.xform.size_access == "--size--"

    def test_size_fmt(self):
        assert self.xform.size_fmt is uint8


class TestPositional:

    xform = SizedX(ascii_greedy, uint8, 2, 10, "size_access", "name")

    def test_fmt(self):
        assert self.xform.fmt is ascii_greedy

    def test_hint(self):
        assert self.xform.__hint__ == "str"

    def test_name(self):
        assert self.xform.name == "name"

    def test_offset(self):
        assert self.xform.offset == 10

    def test_ratio(self):
        assert self.xform.ratio == 2

    def test_size_access(self):
        assert self.xform.size_access == "size_access"

    def test_size_fmt(self):
        assert self.xform.size_fmt is uint8


class TestKeyword(TestPositional):

    xform = SizedX(
        fmt=ascii_greedy,
        size_fmt=uint8,
        ratio=2,
        offset=10,
        size_access="size_access",
        name="name",
    )
