import os


if os.getcwd() == "/content":
    from google.colab.patches import cv2_imshow as imshow
    import cv2
    import requests
    photo_1 = requests.get('https://user-images.githubusercontent.com/100136305/190876998-74c4b591-67ee-458a-b720-ec9e59389cee.jpg')
    out_1 = open("degget_6564.jpeg", "wb")
    out_1.write(photo_1.content)
    out_1.close()
    degget_img = cv2.imread(r"/content/degget_6564.jpeg")
    imshow(degget_img)
else:
    print("Данный метод работает только в Google Colab")
