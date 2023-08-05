import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def installation_require():
    install("requests")


install("setuptools")


