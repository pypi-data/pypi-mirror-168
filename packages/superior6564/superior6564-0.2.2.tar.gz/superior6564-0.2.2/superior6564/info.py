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
    line_need = []
    name_need = ["Name", "Vers", "Desc", "Home", "Down", "Wiki", "Auth", "Lice"]
    with open(path) as f:
        for i in range(19):
            # line = f.readline().replace("\n", "")
            line = f.readline()
            if line[:4] in name_need:
                line_need.append(line)
    with open(path) as f:
        dictionary = {"Name": line_need[0], "Version": line_need[1], "Description": line_need[2],
                      "Home-Page": line_need[3], "Download-URL": line_need[4], "Wiki": line_need[5],
                      "Author": line_need[6], "Author-email": line_need[7], "License": line_need[8]}
        print(dictionary["Name"] + dictionary["Version"] + dictionary["Description"] +
              dictionary["Home-Page"] + dictionary["Download-URL"] + dictionary["Wiki"] +
              dictionary["Author"] + dictionary["Author-email"] + dictionary["License"])
