__author__ = 'gustavosmc'
import base64

def convert_image(str_image):
    with open(str_image, "rb") as file:
        encoded_string = base64.b64encode(file.read())
        string = str(encoded_string)
        output = open("img_base.txt", "w")
        output.writelines(str_image + " -> ")
        output.writelines(string)
        output.close()