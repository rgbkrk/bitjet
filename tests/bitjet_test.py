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

if __name__ == '__main__':
    unittest.main()
