"""

rtflib v. 1.2 Beta
author: lambdaviking

Purpose:
Allows you to write RTF files easily

Example:
The example below generates "helloworld.rtf" that says "hello world" in red:

from rtflib import *
file = RTF("helloworld.rtf")
file.startfile()
file.addstrict()
file.addtext("hello world", color=Color(255,0,0))
file.writeout()

Methods to add to the RTF:
RTF.addstrict() -- adds strict headers to the top of the file
RTF.addelement(element) -- adds an element such as text or a table to the file
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

# define functions that return objects' attributes
render = lambda x: x.__rtfcode__


class Color:
    """Color object"""

    def __init__(self, r=0, g=0, b=0):
        self.red = r
        self.green = g
        self.blue = b


class Format:
    """Object for format (bold, underline, etc.) of text"""

    def __init__(self, bold=False, underline=False, italicized=False, size=24):
        self.bold = bold
        self.underline = underline
        self.italicized = italicized
        self.size = size


class Table:
    """Object for entering a table to the RTF"""

    def __init__(self, color=None, format=None):
        self.color = color
        self.format = format
        self.rows = []
        self.__rtfcode__ = ""
        self.__element__ = "table"

    def addrow(self, row):
        self.rows.append(row)
        self.update()

    def iscompatible(self, type):
        return type == "rtf" or type == "rtfd"

    def update(self):
        # The code doesn't add new lines between rows and puts nearby text into the table as well
        self.__rtfcode__ = ""
        for row in self.rows:
            self.__rtfcode__ += row.render()


class Row:
    """Row of a table
    
    See: https://stackoverflow.com/questions/8349827/using-tables-in-rtf
    """

    def __init__(self):
        self.cells = []

    def addcell(self, cell, color=False, format=False):
        self.cells.append(Line(cell, color, format))
    
    def render(self) -> str:
        rtfcode = "\\trowd"
        for idx, cell in enumerate(self.cells):
            # TODO: Make these parameters.
            rtfcode += f"\\cellx{(idx + 1) * 1000}"
        for cell in self.cells:
            # TODO: Refactor this into cell method.
            # TODO: Allow formatting in table

            rtfcode += f"\\intbl {render(cell)}\\cell\n"

        rtfcode += "\\row\n"
        return rtfcode


class Line:
    """Represents a line of text"""

    def __init__(self, text, color=None, format=None):
        self.format = format
        self.text = text.replace("\n", "\\\n\ ")
        self.__element__ = "line"
        self.color = color
        self.__cid__ = None
        self.__rtfcode__ = self.text

    def iscompatible(self, type):
        return type == "rtf" or type == "rtfd"


class HyperString:
    """Line of meta language added into the RTF"""

    def __init__(self, text):
        self.format = None
        self.color = None
        self.__rtfcode__ = text


class RTF:
    """RTF file object"""

    def __init__(self, name):
        self.name = name
        self.preelements = []
        self.colors = [[0, 0, 0], [255, 255, 255]]
        self.elements = []

    def startfile(self):
        self.preelements.append(
            HyperString("\\rtf1\\ansi\\ansicpg1252\\cocoartf1038\\cocoasubrtf320")
        )

    def addstrict(self):
        self.elements.append(HyperString("\\f0\\fs24\\cf0\n"))

    def addtext(self, text, color=None, format=None):
        self.elements.append(Line(text, color, format))

    def addelement(self, element):
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
            name = getattr(element, "__element__", repr(element))
            raise ValueError(f"element '{name}' incompatible with RTF")

    def writeout(self):
        wf = open(self.name, "w")
        wf.write("{\n")
        for preelement in self.preelements:
            wf.write(render(preelement) + "\n")
        wf.write("{\n")
        wf.write("\\colortbl;\n")
        for color in self.colors:
            wf.write(
                "\\red"
                + str(color[0])
                + "\\green"
                + str(color[1])
                + "\\blue"
                + str(color[2])
                + ";\n"
            )
        wf.write("}\n")
        for element in self.elements:
            if "__cid__" in dir(element):
                wf.write(
                    "\\cf" + (str(element.__cid__) if element.color else "0") + " "
                )
            if element.format and element.format.underline:
                wf.write("\\ul ")
            if element.format and element.format.bold:
                wf.write("\\b ")
            if element.format and element.format.italicized:
                wf.write("\\i ")
            if element.format:
                wf.write("\\fs" + str(element.format.size) + " ")
            wf.write(render(element) + "\n")
            if element.format and element.format.underline:
                wf.write("\\ulnone ")
            if element.format in dir(element) and element.format.bold:
                wf.write("\\b0 ")
            if element.format and element.format.italicized:
                wf.write("\\i0 ")
            if element.format:
                wf.write("\\fs24 ")
            # if "__cid__" in dir(element):
            #     wf.write(r"\\cf0 \ ")
        wf.write("}")
        wf.close()
