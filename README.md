# rtflib
A lightweight Python library for exporting RTFs.

**Have not supported this in 8+ years, since I was in middle school. Still, I believe it should get the trick done in simple use cases.**

## Example usage

```python
from rtflib import Color, RTF

rtf = RTF("helloworld.rtf")
rtf.startfile()
rtf.addstrict()
rtf.addtext("hello world", color=Color(255,0,0))
rtf.writeout()
```
