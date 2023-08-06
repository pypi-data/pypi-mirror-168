import grpc
from ..gRPC_proto.user_proto import user_pb2, user_pb2_grpc, auth_pb2_grpc, auth_pb2


def ChangePassword(channel, params):
    stub = user_pb2_grpc.UserControllerStub(channel)
    response = stub.ChangePassword(
        user_pb2.PasswordRequest(username=params['username'], password=params['password'],
                                 new_password=params['new_password']))
    return response


def ChangeKey(channel, params):
    stub = user_pb2_grpc.UserControllerStub(channel)
    response = stub.ChangeKey(
        user_pb2.KeyRequest(username=params['username'], password=params['password']))
    return response


def GetKey(channel, params):
    stub = user_pb2_grpc.UserControllerStub(channel)
    response = stub.GetKey(
        user_pb2.KeyRequest(username=params['username'], password=params['password']))
    return response


def userLogin(channel, username, password, metadata):
    stub = auth_pb2_grpc.AuthenticationStub(channel)
    print('----- Login -----')
    try:
        response = stub.Login(auth_pb2.LoginRequest(username=username, password=password), metadata=metadata)
        return response
    except grpc.RpcError as e:
        raise Exception('Error ' + str(e.code()) + ': ' + str(e.details()))
