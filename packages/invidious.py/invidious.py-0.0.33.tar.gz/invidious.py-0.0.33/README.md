# Invidious.py
A Python wrapper for Invidious API

# Installation
```pip install invidious.py```

# Getting Started
```py
from invidious import *

iv = Invidious()
searched = iv.search("distrotube")

for item in searched:
    if type(item) == ChannelItem:
        print(item.author) 
        # Print names of all channels
        # in first page of result 'distrotube'
```

# Links
* PyPi: `https://pypi.org/project/invidious.py/`
* Git repo: `https://notabug.org/loliconshik3/invidious.py`
* Matrix: `https://matrix.to/#/#cgwbr:matrix.org`

## Donates
**Monero:** `47KkgEb3agJJjSpeW1LpVi1M8fsCfREhnBCb1yib5KQgCxwb6j47XBQAamueByrLUceRinJqveZ82UCbrGqrsY9oNuZ97xN`
