from .rtf import RtfElement, Line

CODE_DICT = {
    "padding": {"prefix": "\\trpadd", "suffix": "\\trpaddf"},
    "border":  {"prefix": "\\clbrdr", "suffix": "\\brdrs"},
    "dotborder":  {"prefix": "\\clbrdr", "suffix": "\\brdrdot"},
    "dashborder":  {"prefix": "\\clbrdr", "suffix": "\\brdrdash"},
    "doubleborder":  {"prefix": "\\clbrdr", "suffix": "\\brdrdb"}
    }

def _compose_padding(sides: str = "ltrb", size: int = 144):
    """
    Return padding string for row
    """
    code = ""
    for s in sides:
        code += f'{CODE_DICT["padding"]["prefix"]}{s}{size}{CODE_DICT["padding"]["suffix"]}{s}3'
    return code

def _compose_border(sides: str = "ltrb", style: str = "plain"):
    """
    Return border string for row
    """
    style_lookup = {"plain":"border", "dot":"dotborder", "dash":"dashborder", "double":"doubleborder"}
    if style in style_lookup:
        key = style_lookup[style]
    else:
        key = "border"
    code = ""
    for s in sides:
        code += f'{CODE_DICT[key]["prefix"]}{s}{CODE_DICT[key]["suffix"]}'
    return code

class Row(RtfElement):
    """Row of a table
    
    See: https://stackoverflow.com/questions/8349827/using-tables-in-rtf
    """

    def __init__(self, *cells: RtfElement, ends: list[int] = None, borders: str = None, border_style: str="plain",
                 cell_bg=None, padding: str = None, pad_size: int = 144):
        self.cells = cells
        self.padding = ""
        #self.borders = borders

        if ends:
            self.ends = ends
        else:
            self.ends = [(idx + 1) * 1000 for idx in range(len(self.cells))]
        
        if padding:
            self.padding = _compose_padding(padding, pad_size)
        
        if borders:
            self.borders = [_compose_border(borders, border_style) for idx in range(len(self.cells))]
        else:
            self.borders = [""]*len(self.cells)
        
        if cell_bg:
            self.cell_bg = [f"\\clcbpat{cell_bg}" for _ in range(len(self.cells))]
        else:
            self.cell_bg = [""]*len(self.cells)
            
    
    @property
    def rtf_code(self) -> str:
        rtfcode = f"\\trowd{self.padding}\n"
        for end, border, bg in zip(self.ends, self.borders, self.cell_bg):
            rtfcode += f"{border}{bg}\\cellx{end}"
        rtfcode += "\n"
        for cell in self.cells:
            rtfcode += "\\pard\\intbl{" + cell.rtf_code + "}\\cell\n"
        rtfcode += "\\row\n"
        return rtfcode


class Table(RtfElement):
    """Object for entering a table to the RTF"""

    def __init__(self, *rows: Row, ends: list[int] = None):
        """Give rows followed by an optional list of ending positions for cols, in twips"""
        self.rows = rows
        if ends is not None:
            for row in self.rows:
                row.set_widths(ends)

    def iscompatible(self, type):
        return type == "rtf" or type == "rtfd"

    @property
    def rtf_code(self) -> str:
        return "\\\n" + "".join(row.rtf_code for row in self.rows)
