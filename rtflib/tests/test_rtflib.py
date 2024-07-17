import unittest
import os

from .. import *

class TestRtflib(unittest.TestCase):

    def setUp(self):
        self.path = os.path.dirname(__file__)

    def test_hello_world(self):
        rtf = Rtf()
        rtf.add(Line("hello world"))
        with open(os.path.join(self.path, "helloworld.rtf")) as fh:
            self.assertEqual(rtf.rtf_code.strip(), fh.read())

    def test_hello_world_red(self):
        rtf = Rtf()
        rtf.add(Line("hello world", color=Color(255, 0, 0)))
        with open(os.path.join(self.path, "helloworld-red.rtf")) as fh:
            self.assertEqual(rtf.rtf_code.strip(), fh.read())
    
    def test_hello_world_multi(self):
        rtf = Rtf()
        rtf.add(Line("hello world. A Line of text.\n", format=Format(bold=True,strike=True)))
        rtf.add(Line("hello world. A Red line\n", color=Color(255, 0, 0)))
        rtf.add(Line("hello world. A mix of "))
        rtf.add(Line("Green ", color=Color(0, 255, 0)))
        rtf.add(Line("and "))
        rtf.add(Line("Red", color=Color(255, 0, 0)))
        rtf.add(Line(" on a single line.\n"))
        with open(os.path.join(self.path, "helloworld-multi.rtf")) as fh:
            self.assertEqual(rtf.rtf_code.strip(), fh.read())
    
    def test_table(self):
        rtf = Rtf()
        rtf.add(Line("here is a table:"))
        rtf.add(Table(
            Row(Line("hello"), Line("world")),
            Row(Line("hallo"), Line("Welt")),
        ))
        with open(os.path.join(self.path, "table.rtf")) as fh:
            self.assertEqual(rtf.rtf_code.strip(), fh.read())
           
    def test_table_widths(self):
        rtf = Rtf()
        data = [['apple', 121, 'selling'], ['linux', 136, 'borrowing'],
                ['banana', 142, 'buying'], ['cherry', 137, 'borrowing'],
                ['win2k', 147, 'in debt']]
        table_widths = [1500,2100,4500]
        rtf.add(Line("Here is a table with varying widths:\n"))
        rows = [Row(Line(co), Line(f"{val}"), Line(state), ends=table_widths) for co,val,state in data]
        rtf.add(Table(*rows))
        with open(os.path.join(self.path, "table_widths.rtf")) as fh:
            self.assertEqual(rtf.rtf_code.strip(), fh.read())

if __name__ == '__main__':
    unittest.main()