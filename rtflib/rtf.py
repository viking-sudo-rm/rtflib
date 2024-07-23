"""rtflib: A buggy old library for writing RTFs in Python.

See README.md for example usage.

Methods to add to the RTF:
RTF.addstrict() -- adds strict headers to the top of the file
RTF.add(element) -- adds an element such as text or a table to the file
RTF.addtext(text,color=None,format=None) -- a shorthand for adding Line elements to the file with RTF.addelement

Elements:
Elements are objects that can be added to RTFs using this module.

Table -- a table
Row -- a row in a table
Line -- a line of text that can be packed into the file or a Row
HyperString -- a line of custom raw RTF markup to be placed into the file

Descriptor Classes:
Descriptor classes can be passed to the constructor of elements as optional arguments.

Color(r=0,g=0,b=0) -- describes the font color of an element
Format(bold=False,underline=False,intalicized=False,size=24) -- describes the text formatting of an element
"""

from abc import ABCMeta, abstractmethod
from collections import namedtuple

from .format import *


Basecolor = namedtuple(
            "Basecolor",
            "red green blue cid"
            )

class Color(Basecolor):
    """Hold a reference counted rgb color."""
    __slots__ = ()
    @property
    def rtf_code(self):
        return f"\\red{self.red}\\green{self.green}\\blue{self.blue};\n"

  
class RtfElement(metaclass=ABCMeta):
    """Object that can be part of an RTF."""

    @property
    @abstractmethod
    def rtf_code(self):
        raise NotImplementedError


class RtfCode(RtfElement):
    """Line of meta language added into the RTF"""

    def __init__(self, code):
        self.code = code
    
    @property
    def rtf_code(self) -> str:
        return self.code


class Line(RtfElement):
    """Represents a line of text"""

    def __init__(self, text, color=None, format=None):
        self.text = text
        self.color = color
        self.format = format

    def iscompatible(self, type):
        return type == "rtf" or type == "rtfd"

    @property
    def rtf_code(self) -> str:
        code = ""
        if self.color:
            code += f"\\cf{str(self.color.cid)} "
        if self.format:
            code += self.format.code_prefix
        code += self.text.replace("\n", "\\\n\\ ")   
        if self.format:
            code += self.format.code_suffix
        if self.color:
            code += "\\cf0 \\ "
        return code


class Rtf(RtfElement):
    """RTF file object"""

    def __init__(self):
        self.preelements: list[RtfElement] = []
        self.elements: list[RtfElement] = []
        self.colors = []
        self.color_counter = 1  # 0 is reserved

    def addstrict(self):
        self.elements.append(RtfCode("\\f0\\fs24\\cf0\n"))

    def add_color(self, red: int, green: int, blue: int) -> int:
        for c in self.colors:
            if c.red == red and c.green == green and c.blue == blue:
                return c
        # no match found, so append
        c = Color(red, green, blue, self.color_counter)
        self.colors.append(c)
        self.color_counter += 1
        return c
        
    def add(self, element: RtfElement) -> None:
        if element.iscompatible("rtf"):
            self.elements.append(element)
            if "color" in dir(element) and element.color:
                element.color = self.add_color(element.color.red, element.color.green, element.color.blue)
        else:
            raise ValueError(f"element '{type(element).__name__}' incompatible with RTF")
    
    @property
    def rtf_code(self) -> str:
        code = "{\\rtf1\\ansi\\deff0\n"

        for preelement in self.preelements:
            code += preelement.rtf_code + "\n"

        if self.colors:
            code += "{\n"
            code += "\\colortbl;\n"
            for color in self.colors:
                code += color.rtf_code
            code += "}\n"

        for element in self.elements:
            code += element.rtf_code + "\n"

        code += "}"
        return code

    def save(self, wf) -> None:
        """Save to file wf (can be a file pointer or string)"""
        if isinstance(wf, str):
            with open(wf, "w") as fp:
                return self.save(fp)
        wf.write(self.rtf_code)