import base64


def get_base64(path):
    with open(path, "rb") as file:
        my_string = str(base64.b64encode(file.read()).decode('UTF-8'))
    return str(my_string)


def base64ToPDF(b64, filename):
    bytes = base64.b64decode(b64, validate=True)

    # Perform a basic validation to make sure that the result is a valid PDF file
    # Be aware! The magic number (file signature) is not 100% reliable solution to validate PDF files
    # Moreover, if you get Base64 from an untrusted source, you must sanitize the PDF contents
    if bytes[0:4] != b'%PDF':
        raise ValueError('Missing the PDF file signature')

    # Write the PDF contents to a local file
    f = open(filename, 'wb')
    f.write(bytes)
    f.close()

