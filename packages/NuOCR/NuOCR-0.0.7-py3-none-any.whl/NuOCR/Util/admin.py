from ..gRPC_proto.user_proto import user_pb2, user_pb2_grpc


def createUser(channel, params, metadata):
    stub = user_pb2_grpc.UserControllerStub(channel)
    response = stub.Create(
        user_pb2.User(username=params['username'], password=params['password'], email=params['email'],
                      first_name=params['first_name'], last_name=params['last_name']), metadata=metadata)
    return response


def listUser(channel, metadata):
    stub = user_pb2_grpc.UserControllerStub(channel)
    for post in stub.List(user_pb2.UserListRequest(), metadata=metadata):
        print(post, end='')


def retrieveUser(channel, id, metadata):
    stub = user_pb2_grpc.UserControllerStub(channel)
    response = stub.Retrieve(user_pb2.UserRetrieveRequest(id=id), metadata=metadata)
    return response


def updateUser(channel, params, metadata):
    stub = user_pb2_grpc.UserControllerStub(channel)
    response = stub.Update(
        user_pb2.User(username=params['username'], password=params['password'], email=params['email'],
                      first_name=params['first_name'], last_name=params['last_name']), metadata=metadata)
    return response


def deleteUser(channel, params, metadata):
    stub = user_pb2_grpc.UserControllerStub(channel)
    response = stub.Destroy(
        user_pb2.User(username=params['username'], password=params['password'], email=params['email'],
                      first_name=params['first_name'], last_name=params['last_name']), metadata=metadata)
    return response


def AddAccess(channel, params, metadata):
    stub = user_pb2_grpc.UserControllerStub(channel)
    response = stub.AddAccess(
        user_pb2.UserRequest(username=params['username'], access=params['access']), metadata=metadata)
    return response


def RemoveAccess(channel, params, metadata):
    stub = user_pb2_grpc.UserControllerStub(channel)
    response = stub.RemoveAccess(
        user_pb2.UserRequest(username=params['username'], access=params['access']), metadata=metadata)
    return response
