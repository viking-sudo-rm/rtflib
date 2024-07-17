class Color:
    """Color object"""

    def __init__(self, r=0, g=0, b=0):
        self.red = r
        self.green = g
        self.blue = b

PAGE_LAYOUTS = {
    "A4_portrait": "\\pgwsxn11906\\pghsxn16838\\marglsxn720\\margrsxn720\\margtsxn720\\margbsxn720",
    "A4_landscape": "\\lndscpsxn\\pgwsxn16838\\pghsxn11906\\marglsxn720\\margrsxn720\\margtsxn720\\margbsxn720",
    "Letter_portrait": "\\pgwsxn12240\\pghsxn15840\\marglsxn720\\margrsxn720\\margtsxn720\\margbsxn720",
    "Letter_landscape": "\\lndscpsxn\\pgwsxn15840\\pghsxn12240\\marglsxn720\\margrsxn720\\margtsxn720\\margbsxn720"
    }

class Format:
    """Object for format (bold, underline, etc.) of text"""

    def __init__(self, bold=False, underline=False, italicized=False, strike=False, size=24):
        self.bold = bold
        self.underline = underline
        self.italicized = italicized
        self.size = size
        self.strikethrough = strike
    
    @property
    def code_prefix(self) -> str:
        code = ""
        if self.underline:
            code += "\\ul "
        if self.bold:
            code += "\\b "
        if self.italicized:
            code += "\\i "
        if self.strikethrough:
            code += "\\strike "
        code += f"\\fs{str(self.size)} "
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
        if self.strikethrough:
            code += "\\strike0 "
        code += "\\fs24 "
        return code