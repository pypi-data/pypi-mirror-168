import grpc, json
from ..gRPC_proto.extractor_APIs_proto import extractor_pb2, extractor_pb2_grpc


def FormRecognizer(channel, params, metadata):
    stub = extractor_pb2_grpc.ExtractorControllerStub(channel)
    if 'pages' not in params:
        params['pages'] = None
    if 'subscriberId' not in params:
        params['subscriberId'] = ''
    if 'language' not in params:
        params['language'] = ''
    try:
        request = extractor_pb2.FormRequest(base64=params['base64'],
                                            extractionType=params['extractionType'],
                                            mimeType=params['mimeType'],
                                            table=params['table'],
                                            rawJson=params['rawJson'],
                                            pages=params['pages'],
                                            subscriberId=params['subscriberId'],
                                            language=params['language'])
        response = stub.FormRecognition(request, metadata=metadata)
        return json.loads(response.body)
    except grpc.RpcError as e:
        raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))


def DocRecognizer(channel, params, metadata):
    stub = extractor_pb2_grpc.ExtractorControllerStub(channel)
    if 'subscriberId' not in params:
        params['subscriberId'] = ''
    if 'extractionHints' not in params:
        params['extractionHints'] = False
    try:
        request = extractor_pb2.DocRequest(
            base64=params['base64'],
            extractionType=params['extractionType'],
            mimeType=params['mimeType'],
            extractionHints=params['extractionHints'],
            rawJson=params['rawJson'],
            subscriberId=params['subscriberId']
        )
        response = stub.DocAI(request, metadata=metadata)
        return json.loads(response.body)
    except grpc.RpcError as e:
        raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))
