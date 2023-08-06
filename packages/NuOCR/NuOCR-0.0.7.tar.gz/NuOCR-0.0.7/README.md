An API gateway is a software pattern that sits in front of an application programming interface (API) or group of microservices, to facilitate requests and delivery of data and services. Its primary role is to act as a single entry point and standardized process for interactions between an organization's apps, data and services and internal and external customers.

This NuOCR package act as an API gateway which simplifies service delivery and provides flexibility by combining multiple API calls to request and retrieve data and services, which reduces the volume of requests, traffic and manual efforts by great margin.

Advantages are security, reliability, resilience and optimization.

## Installation
To install the NuOCR package, please run the following command in your command line prompt.
```
pip install NuOCR
```

## Examples
Below are few examples, showing the usage of the package. 

1) NuOCR.Util.user
```
import grpc
from NuOCR.Util import user

key_request = {
    'username': "YOUR USERNAME HERE",
    'password': "YOUR PASSWORD HERE"
}

with grpc.insecure_channel("SERVER DOMAIN OR IP HERE") as channel:
    # To fetch the user api-key
    response = user.GetKey(channel, key_request)
    print(response)
    
    # To update the user api-key
    response = user.ChangeKey(channel, key_request)
    print(response)
```

For using the NuOCR services, you need to first register and get the API key or user-credentials, then provide the API-key in the meta-deta to use the following services based on your subscription.
2) NuOCR.Util.extractor

```
import grpc
from NuOCR.Util import extractor

params = {
    "base64": "YOUR BASE64 HERE"
    "extractionType": "invoice" # anyone from ["invoice", "form", "reciept"],
    "mimeType": "application/pdf",
    "table": True, # boolean value
    "rawJson": True # boolean value
}

user_metadata = [('key', 'YOUR API-KEY HERE')]

with grpc.insecure_channel("SERVER DOMAIN OR IP HERE") as channel:
    # To extract document using the DocRecognizer service.
    print('-'*20, 'Recognizer', '-'*20)
    response = extractor.DocRecognizer(channel, params, user_metadata)
    print(response)
    
    # To extract document using the FormRecognizer service.
    print('-'*20, 'Recognizer', '-'*20)
    response = extractor.FormRecognizer(channel, params, user_metadata)
    print(response)
```

Similarly, you can fetch and push data from the IO adaptors using NuOCR.Util.io_adaptor. We have currently integrated S3 and FTP as inbound and outbound adapters.

3) NuOCR.Util.io_adaptor

```
import grpc
from NuOCR.Util import io_adaptor


ftp_param = {
    "host": HOST,
    "port": PORT NUMBER OF THE REMOTE HOST,
    "username": YOUR FTP USERNAME,
    "password": YOUR FTP PASSWORD,
    "isSecure": False, #BOOLEAN VALUE
    "subscriberId": YOUR SUBSCRIBER ID,
    "remoteFolder": SOURCE OR DESTINATION PATH OF FILE,
    "remoteFilename": NAME OF THE FILE YOU WANT TO STORE OR FETCH,
    "base64": YOUR BASE64 HERE
}

s3_params = {
    "subscriberId": YOUR SUBSCRIBER ID,
    "regionName": REGION NAME,
    "accessKey": YOUR ACCESS KEY,
    "secretKey": YOUR SECRET KEY,
    "bucketName": BUCKET NAME,
    "folderName": SOURCE OR DESTINATION PATH,
    "filename": NAME OF THE FILE YOU WANT TO STORE OR FETCH,
    "base64": YOUR BASE64 HERE,
    "localFilename": LOCAL FILE NAME
}

user_metadata = [('key', 'YOUR API-KEY HERE')]

with grpc.insecure_channel("SERVER DOMAIN OR IP HERE") as channel:
    # To fetch document from S3, this will fetch base64 and file name of all files in that directory.
    print('-'*20, 'S3', '-'*20)
    response = io_adaptor.S3InBound(channel, s3_params)
    for i in response:
        print(i.filename, i.base64)
        
    # To push document to FTP, this will push file to destination path.
    print('-'*20, 'FTP', '-'*20)
    response = io_adaptor.FTPOutBound(channel, ftp_param)
    print(response)
```

## Contributing
TBD

## License
TBD
