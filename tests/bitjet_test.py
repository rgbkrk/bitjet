import unittest
import pytest
import sys
import functools

from operator import itemgetter, attrgetter

import bitjet

from IPython.kernel.comm import Comm
from IPython.html.widgets import interact, interactive, Widget, interaction

class DummyComm(Comm):
    comm_id = 'a-b-c-d'

    def open(self, *args, **kwargs):
        pass

    def send(self, *args, **kwargs):
        pass

    def close(self, *args, **kwargs):
        pass

undefined = object()
def raise_not_implemented(*args, **kwargs):
    raise NotImplementedError()

class BitWidgetTest(unittest.TestCase):
    def setUp(self):
        self._widget_attrs = {}
        self._widget_attrs['_comm_default'] = getattr(bitjet.BinaryView, '_comm_default', undefined)
        self._widget_attrs['_ipython_display_'] = bitjet.BinaryView._ipython_display_

        bitjet.BinaryView._comm_default = lambda self: DummyComm()
        bitjet.BinaryView._ipython_display_ = raise_not_implemented

    def tearDown(self):

        for attr, value in self._widget_attrs.items():
            if value is undefined:
                delattr(bitjet.BinaryView, attr)
            else:
                setattr(bitjet.BinaryView , attr, value)

    def test_default_bits_per_block(self):
        bitwidget = bitjet.BitWidget()
        bytewidget = bitjet.ByteWidget()

        self.assertEqual(bitwidget.bits_per_block, 1)
        self.assertEqual(bytewidget.bits_per_block, 8)


if __name__ == '__main__':
    unittest.main()
