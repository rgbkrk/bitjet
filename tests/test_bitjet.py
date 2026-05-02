"""Basic sanity tests. The visual layer lives in JS — these cover the
Python-side plumbing: traitlet types, data coercion, default modes."""

from __future__ import annotations

import pytest
from traitlets import TraitError

from bitjet import BinaryView, BitView, ByteView


def test_bit_view_defaults_to_bit_mode():
    assert BitView().mode == "bit"


def test_byte_view_defaults_to_byte_mode():
    assert ByteView().mode == "byte"


def test_data_accepts_bytes():
    view = BitView(data=b"\x01\x02\x03")
    assert view.data == b"\x01\x02\x03"


def test_data_accepts_bytearray():
    view = BitView(data=bytearray(b"\x01\x02"))
    assert view.data == b"\x01\x02"


def test_data_accepts_memoryview():
    view = BitView(data=memoryview(b"hello"))
    assert view.data == b"hello"


def test_data_accepts_objects_with_tobytes():
    class Fake:
        def tobytes(self) -> bytes:
            return b"\xde\xad\xbe\xef"

    view = BitView(data=Fake())
    assert view.data == b"\xde\xad\xbe\xef"


def test_data_rejects_strings():
    with pytest.raises(TypeError):
        BitView(data="not bytes")  # type: ignore[arg-type]


def test_mode_enum_validates():
    view = BinaryView()
    with pytest.raises(TraitError):
        view.mode = "rainbow"


def test_datawidth_is_int():
    view = BitView(datawidth=128)
    assert view.datawidth == 128


def test_block_size_is_int():
    view = BitView(block_size=8)
    assert view.block_size == 8


def test_empty_data_default():
    view = BitView()
    assert view.data == b""
