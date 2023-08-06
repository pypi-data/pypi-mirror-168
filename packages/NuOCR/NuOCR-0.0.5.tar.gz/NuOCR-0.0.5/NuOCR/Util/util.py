import base64


def get_base64(path):
    with open(path, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
    return str(my_string)
