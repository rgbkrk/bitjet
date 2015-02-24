import mmap

from IPython.html.widgets import DOMWidget
from IPython.utils.traitlets import Int, Unicode, List, Instance, Bytes

import base64

try:
    from numpy import ndarray
except:
    # TODO: wat
    ndarray = None

def b64encode_json(a):
    '''
    Returns a dict containing the base64 encoded a
    '''
    return {'b64data': base64.b64encode(a)}

class BitJetWidget(DOMWidget):
    _view_module = Unicode('nbextensions/bitjet/bitjet', sync=True)
    _model_module = Unicode('nbextensions/bitjet/bitjet', sync=True)
    _model_name = Unicode('BinaryModel', sync=True)

    datawidth = Int(2, sync=True)

    if ndarray:
        data = (
                Bytes(sync=True, to_json=b64encode_json) |
                Instance(ndarray, sync=True, to_json=b64encode_json)
        )
    else:
        data = Bytes(sync=True, to_json=b64encode_json) 

    blockwidth = Int(4, sync=True)
    blockheight = Int(4, sync=True)

class BitWidget(BitJetWidget):
    '''
    BitWidget provides a way to visualize a binary data stream by bits, so long as they
    come in as a bytes array or a numpy array.
    '''
    _view_name = Unicode('BitView', sync=True)

class ByteWidget(BitJetWidget):
    '''
    ByteWidget provides a way to visualize a binary data stream by bytes, so long as they
    come in as a bytes array or a numpy array.
    '''
    _view_name = Unicode('ByteView', sync=True)
