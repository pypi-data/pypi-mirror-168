"""
:authors: Superior_6564
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2022 Superior_6564
"""


import os


def show():
    if os.getcwd() == "/content":
        from google.colab.patches import cv2_imshow as imshow
        import cv2
        import requests
        image_degget = requests.get('https://github.com/Superior-GitHub/Superior6564/raw/main/Images/Degget_6564.jpg')
        out_1 = open("Degget_6564.jpeg", "wb")
        out_1.write(image_degget.content)
        out_1.close()
        degget_img = cv2.imread(r"/content/Degget_6564.jpeg")
        imshow(degget_img)
    else:
        print("Данный метод работает только в Google Colab")
