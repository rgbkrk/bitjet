import mmap

from ipywidgets import DOMWidget
from traitlets import Int, Unicode, List, Instance, Bytes, Enum

import base64

def bytes_to_json(buf, widget):
    """Wrap bytes objects in memoryviews to trigger binary messages."""
    if not buf:
        # temporary workaround since open doesn't support binary serialization
        return None
    return memoryview(buf)

class BinaryView(DOMWidget):
    _view_module = Unicode('nbextensions/bitjet/bitjet', sync=True)
    _view_name = Unicode('BinaryView', sync=True)
    _model_module = Unicode('nbextensions/bitjet/bitjet', sync=True)
    _model_name = Unicode('BinaryModel', sync=True)

    datawidth = Int(8, sync=True)

    data = Bytes(sync=True, to_json=bytes_to_json)

    blockwidth = Int(4, sync=True)
    blockheight = Int(4, sync=True)

    bits_per_block = Enum([1,8], default_value=1, sync=True)
    
    def open(self):
        # workaround ipywidgets bug causing failure to send initial state if it contains binary keys
        _save_data = None
        if self.data:
            _save_data = self.data
            self.data = b''
        super(BinaryView, self).open()
        if _save_data:
            self.data = _save_data

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
