# rtflib
A lightweight Python library for exporting RTFs.

**Have not supported this in 8+ years, since I was in middle school. Still, I believe it should get the trick done in simple use cases.**

## Example usage

```python
from rtflib import Color, RTF

file = RTF("helloworld.rtf")
file.startfile()
file.addstrict()
file.addtext("hello world", color=Color(255,0,0))
file.writeout()
```
