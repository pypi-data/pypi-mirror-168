import base64


def get_base64(path):
    with open(path, "rb") as file:
        my_string = base64.b64encode(file.read())
    return str(my_string)
