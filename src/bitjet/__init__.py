"""bitjet — visualize binary data as fixed-size blocks on a canvas.

Drop a ``bytes``, ``bytearray``, or ``memoryview`` into a ``BitView`` /
``ByteView`` and render it in a Jupyter-compatible notebook. Each bit
(or byte) becomes a fixed-size block, so periodic structure in the
data lines up into columns and patterns are visible at a glance.
"""

from __future__ import annotations

import pathlib

import anywidget
import traitlets

__version__ = "1.0.0"

_HERE = pathlib.Path(__file__).parent


class BinaryView(anywidget.AnyWidget):
    """Base widget for binary-data visualization.

    Subclasses ``BitView`` and ``ByteView`` differ only in their default
    ``mode`` — the underlying widget handles both.

    Parameters
    ----------
    data:
        Binary payload. ``bytes``, ``bytearray``, ``memoryview``, or
        ``numpy.ndarray`` (bytes are taken via ``tobytes()``).
    datawidth:
        Number of units (bits in ``mode="bit"``, bytes in ``mode="byte"``)
        per row of the canvas. Drag the slider in the rendered widget to
        realign periodic patterns.
    block_size:
        Pixel side length of each unit block. Stays constant across
        widths so patterns scale visibly.
    mode:
        ``"bit"`` — each bit is a white (1) or black (0) block.
        ``"byte"`` — each byte is a grayscale block (0=black, 255=white).
    """

    _esm = _HERE / "static" / "bitjet.js"

    data = traitlets.Bytes().tag(sync=True)
    datawidth = traitlets.Int(64).tag(sync=True)
    block_size = traitlets.Int(4).tag(sync=True)
    mode = traitlets.Enum(["bit", "byte"], default_value="bit").tag(sync=True)

    def __init__(
        self,
        data: bytes | bytearray | memoryview | None = None,
        datawidth: int = 64,
        block_size: int = 4,
        mode: str | None = None,
    ) -> None:
        kwargs: dict[str, object] = {
            "data": _coerce(data),
            "datawidth": datawidth,
            "block_size": block_size,
        }
        if mode is not None:
            kwargs["mode"] = mode
        super().__init__(**kwargs)


class BitView(BinaryView):
    """Render a byte string as a bitmap. One bit per block."""


class ByteView(BinaryView):
    """Render a byte string as grayscale. One byte per block."""

    mode = traitlets.Enum(["bit", "byte"], default_value="byte").tag(sync=True)


def _coerce(data: object) -> bytes:
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if isinstance(data, (bytearray, memoryview)):
        return bytes(data)
    tobytes = getattr(data, "tobytes", None)
    if callable(tobytes):
        return bytes(tobytes())
    raise TypeError(f"bitjet data must be bytes-like; got {type(data).__name__}")


__all__ = ["BinaryView", "BitView", "ByteView"]
