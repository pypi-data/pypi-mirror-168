# PY-GUI

Create a pygame session for specific functions

## install

From PyPI:

`pip3 install PY_GUI`

From GitHub:

`pip3 install git+https://github.com/donno2048/PY-GUI`

## Usage

You can use the demo one by running:

```bat
python3 -m PY_GUI
```

Or just `PY-GUI` in the cmd

Or you can run a custom one from within Python, for example:

```py
from PY_GUI import Main
def parse(text: str) -> str:
  return text
Main(parse, name = "Cat program")
```
