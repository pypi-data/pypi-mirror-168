"""
:authors: Superior_6564
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2022 Superior_6564
"""
import os
import requests


readme_md = requests.get('https://raw.githubusercontent.com/Superior-GitHub/superior6564/main/README.md')
out_1 = open("readme.md", "wb")
out_1.write(readme_md.content)
out_1.close()


def get_information():
    with open("readme.md") as f:
        version = f.readline()[22:].strip()
    if os.getcwd() == "/content":
        path = "/usr/local/lib/python3.7/dist-packages/superior6564-" + version + ".dist-info/METADATA"
        with open(path) as f:
            f.readline()
            dictionary = {"Name": f.readline(), "Version": f.readline(), "Summary": f.readline(),
                          "Home-Page": f.readline(), "Author": f.readline(), "Author-email": f.readline(),
                          "License": f.readline(), "Download-URL": f.readline(), }
            print(dictionary["Name"] + dictionary["Version"] + dictionary["Home-Page"] +
                  dictionary["Author"] + dictionary["Author-email"] + dictionary["License"] +
                  dictionary["Download-URL"] + dictionary["Summary"][9:] +
                  "In the wiki you will be told how to use the functions of library superior6564: https://github.com/Superior-GitHub/superior6564/wiki")
get_information()
