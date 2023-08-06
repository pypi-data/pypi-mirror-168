"""
:authors: Superior_6564
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2022 Superior_6564
"""
import subprocess
import sys
import time


def install(package: str, check=True):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
    if check:
        print(f"Library {package} installed.")


def pip_upgrade():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])


def required():
    install("python-time", check=False)
    require = ["requests", "ipython", "progress", "dearpygui"]
    print("Installing the required libraries...")
    for i in range(len(require)):
        install(require[i])
        print(f"Status: {i + 1} of {len(require)}")
        time.sleep(1)
    print("Installation is complete.")
