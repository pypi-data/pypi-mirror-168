"""
:authors: Superior_6564
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2022 Superior_6564
"""
import os
import requests


with open("readme.md", "wb") as f:
    f.write(requests.get('https://raw.githubusercontent.com/Superior-GitHub/superior6564/main/README.md').content)


def get_info():
    path = os.getcwd() + "/readme.md"
    with open(path) as f:
        dictionary = {"Name": f.readline(), "Version": f.readline(), "Description": f.readline(),
                      "Home-Page": f.readline(), "Download-URL": f.readline(), "Wiki": f.readline(),
                      "Author": f.readline(), "Author-email": f.readline(), "License": f.readline()}
        print(dictionary["Name"] + dictionary["Version"] + dictionary["Description"] +
              dictionary["Home-Page"] + dictionary["Download-URL"] + dictionary["Wiki"] +
              dictionary["Author"] + dictionary["Author-email"] + dictionary["License"])
