import unittest
import os

from rtflib import *

HELLO_WORLD = """
{\\rtf1\\ansi\\deff0
hello world
}
"""

HELLO_WORLD_RED = """
{\\rtf1\\ansi\\deff0
{
\\colortbl;
\\red255\\green0\\blue0;
}
\\cf1 hello world\\cf0 \\ 
}
"""

TABLE = """
{\\rtf1\\ansi\\deff0
here is a table:
\\trowd\\cellx1000\\cellx2000
\\pard\\intbl{hello}\\cell
\\pard\\intbl{world}\\cell
\\row
\\trowd\\cellx1000\\cellx2000
\\pard\\intbl{hallo}\\cell
\\pard\\intbl{Welt}\\cell
\\row

}
"""

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
    
    def test_table(self):
        rtf = Rtf()
        rtf.add(Line("here is a table:"))
        rtf.add(Table(
            Row(Line("hello"), Line("world")),
            Row(Line("hallo"), Line("Welt")),
        ))
        with open(os.path.join(self.path, "table.rtf")) as fh:
            self.assertEqual(rtf.rtf_code.strip(), fh.read())

if __name__ == '__main__':
    unittest.main()