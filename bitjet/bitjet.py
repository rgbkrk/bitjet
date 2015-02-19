import mmap

from IPython.html.widgets import DOMWidget
from IPython.utils.traitlets import Int, Unicode, List

class BitWidget(DOMWidget):
    _view_module = Unicode('nbextensions/bitjet/bitjet', sync=True)
    _view_name = Unicode('BitView', sync=True)


    bitwidth = Int(2, sync=True)
    data = List([True, False, True, False], sync=True)
    blockwidth = Int(4, sync=True)
    blockheight = Int(4, sync=True)


#class FileView(BitWidget):
#    
#    def __init__(self, filename):
#        # TODO: Figure out proper way to extend Widgets
#        self.fh = open(filename,"rb")
#        self.m = mmap.mmap(self.fh.fileno(), 0, access=mmap.ACCESS_READ)
#        ba = bytearray(m)
#        np.array(ba)
