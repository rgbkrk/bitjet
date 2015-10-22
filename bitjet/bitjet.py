import mmap

from ipywidgets import DOMWidget
from traitlets import Int, Unicode, List, Instance, Bytes, Enum

import base64

class BinaryView(DOMWidget):
    _view_module = Unicode('nbextensions/bitjet/bitjet', sync=True)
    _view_name = Unicode('BinaryView', sync=True)
    _model_module = Unicode('nbextensions/bitjet/bitjet', sync=True)
    _model_name = Unicode('BinaryModel', sync=True)

    datawidth = Int(2, sync=True)

    data = Bytes(sync=True)

    blockwidth = Int(4, sync=True)
    blockheight = Int(4, sync=True)

    bits_per_block = Enum([1,8], default_value=1, sync=True)

class BitWidget(BinaryView):
    '''
    BitWidget provides a way to visualize a binary data stream by bits, so long as they
    come in as a bytes array or a numpy array.
    '''
    pass

class ByteWidget(BinaryView):
    '''
    ByteWidget provides a way to visualize a binary data stream by bytes, so long as they
    come in as a bytes array or a numpy array.
    '''
    bits_per_block = Enum([1,8], default_value=8, sync=True)
