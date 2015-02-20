import mmap

from IPython.html.widgets import DOMWidget
from IPython.utils.traitlets import Int, Unicode, List, Instance, Bytes

class BitWidget(DOMWidget):
    _view_module = Unicode('nbextensions/bitjet/bitjet', sync=True)
    _view_name = Unicode('BitView', sync=True)

    bitwidth = Int(2, sync=True)

    data = List(Int(), sync=True) # | Bytes(sync=True) # | Instance(bytearray, sync=True)

    blockwidth = Int(4, sync=True)
    blockheight = Int(4, sync=True)
