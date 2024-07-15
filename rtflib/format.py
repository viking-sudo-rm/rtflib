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
    
    @property
    def code_prefix(self) -> str:
        code = ""
        if self.underline:
            code += "\\ul "
        if self.bold:
            code += "\\b "
        if self.italicized:
            code += "\\i "
        code += "\\fs" + str(self.format.size) + " "
        return code

    @property
    def code_suffix(self) -> str:
        code = ""
        if self.underline:
            code += "\\ulnone "
        if self.bold:
            code += "\\b0 "
        if self.italicized:
            code += "\\i0 "
        code += "\\fs24 "
        return code