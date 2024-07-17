# rtflib
A lightweight Python library for exporting RTFs.

**I wrote this in middle school more than 10 years ago and have only lightly supported it since. Still, it could get the job done in simple use cases.**

If you extend the library, feel free to open a pull request! Here is a [reference on RTF syntax](https://www.oreilly.com/library/view/rtf-pocket-guide/9781449302047/ch01.html) which may be helpful for adding features.

## Example usage

Hello world example:

```python
from rtflib import Rtf, Line
rtf = Rtf()
rtf.add(Line("hello world"))
rtf.save("rtflib/tests/helloworld.rtf")
```

The same but in red:

```python
from rtflib import Rtf, Line, Color
rtf = Rtf()
rtf.add(Line("hello world", color=Color(255, 0, 0)))
rtf.save("rtflib/tests/helloworld-red.rtf")
```

Table example:

```python
from rtflib import Rtf, Table, Row, Line
rtf = Rtf()
rtf.add(Line("here is a table:"))
rtf.add(Table(
    Row(Line("hello"), Line("world")),
    Row(Line("hallo"), Line("Welt")),
))
rtf.save("rtflib/tests/table.rtf")
```

## Running tests

From the root of the repository, run:

```shell
pytest
```

Tests will also be run automatically when a pull request is created.