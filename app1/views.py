from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from authUser.models import User


# Create your views here.


@api_view(["POST"])
@permission_classes([AllowAny])
def CreateGroup(request):
    print(request.data);
    data = request.data
    user_id = User.objects.get(id=data['created_by'])
    group = Group.objects.create(name=data['name'], description=data['description'], created_by=user_id)
    group.save()
    g = Group.objects.get(id=group.id)
    code = "SCR" + "{:04}".format(group.id)
    g.code = code
    g.save()
    message = {'save': True}
    return Response(message)


# {
#     "name": "group1",
#     "description": "demo",
#     "created_by": "user_id"
# }


@api_view(["POST"])
@permission_classes([AllowAny])
def JoinGroup(request):
    print(request.data)
    data = request.data
    user_id = User.objects.get(id=data['user_id'])

    group_id = Group.objects.get(code=data['code'])
    print(group_id)
    print("-------------")
    # return Response({})
    #
    if group_id.is_active:
        # print("-------------")

        group_user = GroupUser.objects.create(user_id=user_id, group_id=group_id)
        group_user.save()
        message = {'join': True, 'group': {'id': group_id.id, 'name': group_id.name, 'code': group_id.code}}
    else:
        message = {'join': False, 'message': 'group is not active'}
    return Response(message)


# {
#     "code": "SCR0001",
#     "user_id": 3
# }


@api_view(["GET"])
@permission_classes([AllowAny])
def JoinedGroup(request, user_id):
    user = User.objects.get(id=user_id)
    gu = GroupUser.objects.filter(user_id=user)
    groups = []
    d = [e for e in gu]
    for data in d:
        if data.group_id.is_active:
            group = {
                'id': data.group_id.id,
                'name': data.group_id.name,
                'code': data.group_id.code,
                'description': data.group_id.description,
                'created_at': data.group_id.created_at,
            }
            groups.append(group)

    return Response(groups)


@api_view(["GET"])
@permission_classes([AllowAny])
def CreatedGroup(request, user_id):
    user = User.objects.get(id=user_id)
    grp = Group.objects.filter(created_by=user)
    groups = []
    d = [e for e in grp]
    for data in d:
        if data.is_active:
            group = {
                'id': data.id,
                'name': data.name,
                'code': data.code,
                'description': data.description,
                'created_at': data.created_at,
            }
            groups.append(group)
        else:
            continue

    return Response(groups)


@api_view(["GET"])
@permission_classes([AllowAny])
def GroupInfo(request, group_id):
    data = Group.objects.get(id=group_id)
    group = {
        'id': data.id,
        'name': data.name,
        'code': data.code,
        'description': data.description,
        'created_at': data.created_at,
    }

    return Response(group)


@api_view(["GET"])
@permission_classes([AllowAny])
def DeactivateGroup(request, group_id):
    data = Group.objects.get(id=group_id)
    if data.is_active:
        data.is_active = False
        data.save()
    message = {'deactivate': True}
    return Response(message)


@api_view(["GET"])
@permission_classes([AllowAny])
def StreamScreen(request, group_id):
    message = {'message': 'demo'}
    return Response(message)


@api_view(["POST"])
@permission_classes([AllowAny])
def UploadFile(request):
    print(request.POST)
    data = request.POST
    group_id = Group.objects.get(id=data['group_id'])
    file = File.objects.create(book=request.FILES['file'], group_id=group_id)
    file.save()
    message = {'save': True}
    return Response(message)


# {
#     "group_id": 1,
#     "file": "demo",
# }

@api_view(["GET"])
@permission_classes([AllowAny])
def GroupFiles(request, group_id):
    group_id = Group.objects.get(id=group_id)
    file = File.objects.values("id", "book").filter(group_id=group_id)
    # message = {'save': True}
    return Response(file)
