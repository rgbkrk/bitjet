from IPython.html.widgets import DOMWidget
from IPython.utils.traitlets import Int, Unicode, List

class BitWidget(DOMWidget):
    _view_module = Unicode('nbextensions/bitjet', sync=True)
    _view_name = Unicode('BitView', sync=True)


    bitwidth = Int(2, sync=True)
    data = List([True, False, True, False], sync=True)
