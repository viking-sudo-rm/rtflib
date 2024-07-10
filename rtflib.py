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

#define functions that return objects' attributes
render = lambda x: x.__rtfcode__
show = lambda x: x.__element__

#custom error type "ElementError"
class ElementError(Exception):
	pass

#color object for input
class Color:
	"""color object"""
	def __init__(self,r=0,g=0,b=0):
		self.red = r
		self.green = g
		self.blue = b

#format (bold, underline, etc.) object for input
class Format:
	"""object for format (bold, underline, etc.) of text"""
	def __init__(self,bold=False,underline=False,italicized=False,size=24):
		self.bold = bold
		self.underline = underline
		self.italicized = italicized
		self.size = size

#object for entering a table to the RTF
class Table:
	"""table object"""
	def __init__(self,color=None,format=None):
		self.color = color
		self.format = format
		self.rows = []
		self.__rtfcode__ = ""
		self.__element__ = "table"
	def addrow(self,row):
		self.rows.append(row)
		self.update()
	def iscompatible(self,type):
		return type == "rtf" or type == "rtfd"
	def update(self):
		for row in self.rows:
			self.__rtfcode__ += "\\itap1\\trowd \\taflags1 \\trgaph108\\trleft-108 \\trbrdrt\\brdrnil \\trbrdrl\\brdrnil \\trbrdrr\\brdrnil\n"
			for cell in row.cells:
				if "__cid__" in dir(cell): self.__rtfcode__ += "\\cf" + (str(cell.__cid__) if cell.color else "0") + " "
				if cell.format and cell.format.underline: self.__rtfcode__ += "\\ul "
				if cell.format and cell.format.bold: self.__rtfcode__ += "\\b "
				if cell.format and cell.format.italicized: self.__rtfcode__ += "\\i "
				self.__rtfcode__ += render(cell) + "\n"
				if cell.format and cell.format.underline: self.__rtfcode__ += "\\ulnone "
				if cell.format in dir(cell) and cell.format.bold: self.__rtfcode__ += "\\b0 "
				if cell.format and cell.format.italicized: self.__rtfcode__ += "\\i0 "
				if "__cid__" in dir(cell): self.__rtfcode__ += r"\\cf0 \ "
			self.__rtfcode__ += "\\row\n"

#object for row of a table
class Row:
	"""row of a table"""
	def __init__(self):
		self.cells = []
	def addcell(self,cell,color=False,format=False):
		self.cells.append(Line(cell,color,format))

#object for entering a string of text to the RTF
class Line:
	"""line of text object"""
	def __init__(self,text,color=None,format=None):
		self.format = format
		self.text = text.replace("\n",r"\\\n\ ")
		self.__element__ = "line"
		self.color = color; self.__cid__ = None
		self.__rtfcode__ = self.text
	def iscompatible(self,type):
		return type == "rtf" or type == "rtfd"

#object for embedded line of text in the RTF
class HyperString:
	"""line of text used in RTF class"""
	def __init__(self,text):
		self.format = None
		self.color = None
		self.__rtfcode__ = text

#RTF file class
class RTF:
	"""RTF file object"""
	def __init__(self,name):
		self.name = name
		self.preelements = []
		self.colors = [[0,0,0],[255,255,255]]
		self.elements = []
	def startfile(self):
		self.preelements.append(HyperString("\\rtf1\\ansi\\ansicpg1252\\cocoartf1038\\cocoasubrtf320"))
	def addstrict(self):
		self.elements.append(HyperString("\\f0\\fs24\\cf0\n"))
	def addtext(self,text,color=None,format=None):
		self.elements.append(Line(text,color,format))
	def addelement(self,element):
		try:
			if element.iscompatible("rtf"):
				self.elements.append(element)
				if "color" in dir(element) and element.color:
					if not [element.color.red,element.color.green,element.color.blue] in self.colors:
						self.colors.append([element.color.red,element.color.green,element.color.blue])
					element.__cid__ = self.colors.index([element.color.red,element.color.green,element.color.blue]) + 1
			else:
				raise ElementError("element '" + show(element) + "' incompatible with class 'RTF'")
		except ZeroDivisionError:
			raise ElementError("invalid element: '" + repr(element) + "'")
	def writeout(self):	
		wf = open(self.name,"w")
		wf.write("{")
		for preelement in self.preelements:
			wf.write(render(preelement) + "\n")
		wf.write("{")
		wf.write("\\colortbl;\n")
		for color in self.colors:
			wf.write("\\red" + str(color[0]) + "\\green" + str(color[1]) + "\\blue" + str(color[2]) + ";\n")
		wf.write("}\n")
		for element in self.elements:
			if "__cid__" in dir(element): wf.write("\\cf" + (str(element.__cid__) if element.color else "0") + " ")
			if element.format and element.format.underline: wf.write("\\ul ")
			if element.format and element.format.bold: wf.write("\\b ")
			if element.format and element.format.italicized: wf.write("\\i ")
			if element.format: wf.write("\\fs" + str(element.format.size) + " ")
			wf.write(render(element) + "\n")
			if element.format and element.format.underline: wf.write("\\ulnone ")
			if element.format in dir(element) and element.format.bold: wf.write("\\b0 ")
			if element.format and element.format.italicized: wf.write("\\i0 ")
			if element.format: wf.write("\\fs24 ")
			if "__cid__" in dir(element): wf.write(r"\cf0 \ ")
		wf.write("}")
		wf.close()

if __name__ == "__main__":
	file = RTF("helloworld.rtf")
	file.startfile()
	file.addstrict()
	file.addtext("hello world", color=Color(255,0,0))
	#file.addelement((Table(color=Color(255,255,0))))
	file.writeout()
