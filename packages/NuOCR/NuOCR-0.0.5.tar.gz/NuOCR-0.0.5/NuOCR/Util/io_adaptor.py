from ..gRPC_proto.io_adaptors_APIs_proto import io_adaptors_pb2, io_adaptors_pb2_grpc


def FTPInBound(channel, param, metadata):
    stub = io_adaptors_pb2_grpc.IOAdaptorControllerStub(channel)
    response = stub.FTPInBound(
        io_adaptors_pb2.FTPRequest(host=param['host'], port=param['port'], username=param['username'],
                                   password=param['password'], isSecure=param['isSecure'],
                                   subscriberId=param['subscriberId'],
                                   remoteFolder=param['remoteFolder'], remoteFilename=param['remoteFilename'],
                                   base64=param['base64']
                                   ), metadata=metadata
    )
    return response


def FTPOutBound(channel, param, metadata):
    stub = io_adaptors_pb2_grpc.IOAdaptorControllerStub(channel)
    response = stub.FTPOutBound(
        io_adaptors_pb2.FTPRequest(host=param['host'], port=param['port'], username=param['username'],
                                   password=param['password'], isSecure=param['isSecure'],
                                   subscriberId=param['subscriberId'],
                                   remoteFolder=param['remoteFolder'], remoteFilename=param['remoteFilename'],
                                   base64=param['base64']), metadata=metadata)
    return response.status


def S3InBound(channel, params, metadata):
    stub = io_adaptors_pb2_grpc.IOAdaptorControllerStub(channel)
    response = stub.S3InBound(
        io_adaptors_pb2.S3Request(
            subscriberId=params['subscriberId'], regionName=params['regionName'], accessKey=params['accessKey'],
            secretKey=params['secretKey'], bucketName=params['bucketName'], folderName=params['folderName'],
            filename=params['filename'], base64=params['base64'], localFilename=params['localFilename'],
        ), metadata=metadata
    )
    return response


def S3OutBound(channel, params, metadata):
    stub = io_adaptors_pb2_grpc.IOAdaptorControllerStub(channel)
    response = stub.S3OutBound(
        io_adaptors_pb2.S3Request(
            subscriberId=params['subscriberId'], regionName=params['regionName'], accessKey=params['accessKey'],
            secretKey=params['secretKey'], bucketName=params['bucketName'], folderName=params['folderName'],
            filename=params['filename'], base64=params['base64'], localFilename=params['localFilename'],
        ), metadata=metadata
    )
    return response.status

