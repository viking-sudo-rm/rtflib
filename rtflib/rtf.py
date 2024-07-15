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

from .format import *


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


class Line:
    """Represents a line of text"""

    def __init__(self, text, color=None, format=None):
        self.text = text
        self.color = color
        self.format = format
        self.__cid__ = None

    def iscompatible(self, type):
        return type == "rtf" or type == "rtfd"

    @property
    def rtf_code(self) -> str:
        code = ""
        if self.__cid__ is not None:
            code += f"\\cf{str(self.__cid__)} "
        if self.format:
            code += self.format.code_prefix
        code += self.text.replace("\n", "\\\n\\ ")   
        if self.format:
            code += self.format.code_suffix
        if self.__cid__ is not None:
            code += "\\cf0 \\ "
        return code


class Rtf(RtfCode):
    """RTF file object"""

    def __init__(self):
        self.preelements: list[RtfElement] = []
        self.elements: list[RtfElement] = []
        self.colors = []

    def addstrict(self):
        self.elements.append(RtfCode("\\f0\\fs24\\cf0\n"))

    def add(self, element: RtfElement) -> None:
        if element.iscompatible("rtf"):
            self.elements.append(element)
            if "color" in dir(element) and element.color:
                if (
                    not [element.color.red, element.color.green, element.color.blue]
                    in self.colors
                ):
                    self.colors.append(
                        [element.color.red, element.color.green, element.color.blue]
                    )
                element.__cid__ = (
                    self.colors.index(
                        [element.color.red, element.color.green, element.color.blue]
                    )
                    + 1
                )
        else:
            raise ValueError(f"element '{type(element).__name__}' incompatible with RTF")

    @property
    def rtf_code(self) -> str:
        code = "{\\rtf1\\ansi\\deff0\n"

        for preelement in self.preelements:
            code + preelement.rtf_code + "\n"

        if self.colors:
            code += "{\n"
            code += "\\colortbl;\n"
            for color in self.colors:
                code += f"\\red{str(color[0])}\\green{str(color[1])}\\blue{str(color[2])};\n"
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