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

HELLO_WORLD_MULTI = """
{\rtf1\ansi\deff0
{
\colortbl;
\red255\green0\blue0;
\red0\green255\blue0;
}
hello world. A Line of text.\
\ 
\cf1 hello world. A Red line\
\ \cf0 \ 
hello world. A mix of 
\cf2 Green \cf0 \ 
and 
\cf1 Red\cf0 \ 
 on a single line.\
\ 
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
    
    def test_hello_world_multi(self):
        rtf = Rtf()
        rtf.add(Line("hello world. A Line of text.\n"))
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

if __name__ == '__main__':
    unittest.main()