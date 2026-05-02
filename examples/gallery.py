"""Gallery of bitjet use cases. Run in Jupyter / nteract / VS Code notebooks.

Each ``display(...)`` below shows a different kind of structure in the bits.
Drag the width slider to shift the tiling and watch periodic patterns appear.
"""

import os
import pickle

from IPython.display import display

from bitjet import BitView, ByteView

# Byte gradient 0..255, tiled 16x. In byte mode this is a smooth grayscale
# ramp; in bit mode each byte's bit pattern is visible, and tiling periodicity
# shows up whenever datawidth is a multiple of 8.
display(ByteView(data=bytes(range(256)) * 16, datawidth=32, block_size=6))

# Pure entropy — looks like noise at any width, at any block size.
display(BitView(data=os.urandom(8192), datawidth=128, block_size=2))

# ASCII text. Low-bit nibbles carry the characters, high bits are mostly
# 0x60/0x70. Try sliding datawidth around 8, 16, 64.
display(
    BitView(
        data=("The quick brown fox jumps over the lazy dog. " * 128).encode(),
        datawidth=64,
    )
)

# Pickle dump — format headers, string runs, and null padding are all visible.
# Try width=40 to align the protocol's framing.
display(
    BitView(
        data=pickle.dumps({str(i): list(range(i)) for i in range(128)}),
        datawidth=40,
    )
)

# Sanity check: MSB-first bit order. One byte with only the top bit set,
# rest zero. At datawidth=8 the top-left block should be the only lit one.
buf = bytearray(64)
buf[0] = 0b10000000
display(BitView(data=bytes(buf), datawidth=8, block_size=10))
