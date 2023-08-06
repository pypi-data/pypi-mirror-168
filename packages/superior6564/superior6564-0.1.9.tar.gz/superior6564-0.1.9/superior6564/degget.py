"""
:authors: Superior_6564
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2022 Superior_6564
"""
from IPython.display import Image, display
import requests


with open("degget_elite.jpg", "wb") as f:
    f.write(requests.get('https://github.com/Superior-GitHub/superior6564/raw/main/superior6564/degit_Elite.jpg').content)


def show(check: int):
    if check == 1:
        display(Image(filename="degget_elite.jpg"))
    elif check == 0:
        print("This method only works in web compilers")

