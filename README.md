# rtflib
A lightweight Python library for exporting RTFs.

**Have not supported this in 8+ years, since I was in middle school. Still, I believe it should get the trick done in simple use cases.**

## Example usage

Hello world example:

```python
from rtflib import Color, RTF

rtf = RTF("helloworld.rtf")
rtf.startfile()
rtf.addstrict()
rtf.addtext("hello world", color=Color(255,0,0))
rtf.writeout()
```

Table example:

```python
from rtflib import RTF, Table, Row
rtf = RTF("table.rtf")
rtf.addtext("hello world")

table = Table()
row1 = Row()
row1.addcell("hello")
row1.addcell("world")
table.addrow(row1)
row2 = Row()
row2.addcell("hallo")
row2.addcell("Welt")
table.addrow(row2)
rtf.addelement(table)
rtf.writeout()
```