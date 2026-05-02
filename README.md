# bitjet

Binary data visualization as a Jupyter anywidget. Drop bytes in, see structure come out.

```python
from bitjet import BitView, ByteView

BitView(data=open("/bin/ls", "rb").read(), datawidth=64)
```

![bitjet screenshot](docs/screenshot.png)

## What it does

Every bit (or byte) in your payload becomes a fixed-size block on a canvas. The `datawidth` slider changes how many units are drawn per row — not how big the canvas gets — so periodic structures in the data (byte boundaries in ASCII text, alignment padding, null runs in executables, LZ-compressed block headers) line up into columns and patterns pop out as you drag.

## Install

```bash
pip install bitjet
```

That's it. anywidget handles the JS — no lab extension, no server extension, no rebuild step.

## Use

```python
from bitjet import BitView, ByteView

# Bit mode: each bit is a white (1) or black (0) block. Good for ASCII text,
# checksums, bitfields, anywhere the individual bits matter.
BitView(data=b"The quick brown fox jumps over the lazy dog. " * 128, datawidth=64)

# Byte mode: each byte is a grayscale block (0=black, 255=white). Good for
# pixel data, pickled objects, compressed blobs, anything where byte-level
# entropy matters.
ByteView(data=bytes(range(256)) * 16, datawidth=32, block_size=6)
```

Assign to `data` to live-update:

```python
import os

view = BitView(data=b"")
view  # renders

# In a later cell
view.data = os.urandom(8192)
```

## Traitlets

| trait | type | default | meaning |
|-------|------|---------|---------|
| `data` | `bytes` | `b""` | The binary payload. Accepts `bytes`, `bytearray`, `memoryview`, or anything with `.tobytes()` (e.g. `numpy.ndarray`). |
| `datawidth` | `int` | `64` | Units per row. Bits if `mode == "bit"`, bytes if `mode == "byte"`. |
| `block_size` | `int` | `4` | Pixel side length of each unit. Fixed across widths so patterns scale. |
| `mode` | `"bit"` or `"byte"` | `"bit"` | Rendering mode. |

All sync bidirectionally. Drag the slider and the Python side sees the update; assign `view.datawidth = 128` and the canvas redraws.

## Compatible with

- JupyterLab 3+
- Jupyter Notebook 7+
- VS Code notebooks
- nteract desktop (tested during development)
- Anything else that runs anywidget

## History

Replaces the original 2014-era [bitjet](https://pypi.org/project/bitjet/) that
depended on ipywidgets 1.x-style nbextensions. Same idea, modern plumbing —
anywidget loads the ESM directly instead of requiring a notebook extension
install.

## License

BSD-3-Clause. See [LICENSE](LICENSE).
