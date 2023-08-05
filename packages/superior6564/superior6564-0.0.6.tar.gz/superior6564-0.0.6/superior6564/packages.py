"""
:authors: Superior_6564
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2022 Superior_6564
"""

import subprocess
import sys
import os


def install(package: str, check=True):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
    if check:
        if os.getcwd() == "/content":
            package = "pip show " + package
            get_ipython().system(package)


def pip_upgrade():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])


def required():
    print("Установка необходимых библиотек")
    install("requests", check=False)
    install("opencv-python", check=False)
    print("Установка завершена")
