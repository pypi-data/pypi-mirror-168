"""
:authors: Superior_6564
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2022 Superior_6564
"""

import subprocess
import sys
import os
import time


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
    install("python-time", check=False)
    require = ["requests", "opencv-python", "progress", "dearpygui"]
    print("Установка необходимых библиотек...")
    for i in range(len(require)):
        install(require[i], check=False)
        print(f"Status: {i + 1} of {len(require)}")
    print("Установка завершена.")
    time.sleep(1)
