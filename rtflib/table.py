from .rtf import RtfElement, Line


class Row(RtfElement):
    """Row of a table
    
    See: https://stackoverflow.com/questions/8349827/using-tables-in-rtf
    """

    def __init__(self, *cells: RtfElement, ends: list[int] = None):
        self.cells = cells

        if ends:
            self.ends = ends
        else:
            self.ends = [(idx + 1) * 1000 for idx in range(len(self.cells))]
    
    @property
    def rtf_code(self) -> str:
        rtfcode = "\\trowd\n"
        for end, cell in zip(self.ends, self.cells):
            rtfcode += f"\\cellx{end}"
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
