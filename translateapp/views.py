import os
from rest_framework.decorators import api_view, permission_classes
import Model
from rest_framework.response import Response
import json
from .serializers import *
from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import AppUser
from .dataset_manager import DataSetManager


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def translate(request):
    translator = Model.translate.TranslationModeBuilder().load(os.path.join("saved-files"))
    translation = translator.evaluate(request.data["pseudo"])
    return Response(json.dumps(translation))


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        error_messages = [str(err) for val in serializer.errors.values() for err in val]
        return Response("\n".join(error_messages), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def up_vote(request):
    """
    handle the event of user up voting
    :param request: the request sent
    :return: 201 response if user is approved, else forbidden
    """
    user = AppUser.objects.get(username=request.user.username)
    if user.status == AppUser.APPROVED:
        DataSetManager.suggest(request.data["translation"], request.data["translation"], user, False)
        return Response(status=202)
    if user.status == AppUser.UNVERIFIED:
        return Response("Please verify your email in order to up vote", 403)
    return Response("Due to bad feedback on your suggestions and votes, tour user is currently unable to vote", 403)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def suggest(request):
    """
    handle the event of user suggesting a new translation
    :param request: the request sent
    :return: 201 response if user is approved, else forbidden
    """
    user = AppUser.objects.get(username=request.user.username)
    if user.status == AppUser.APPROVED:
        DataSetManager.suggest(request.data["origin"], request.data["suggestion"], user)
        return Response(status=202)
    if user.status == AppUser.UNVERIFIED:
        return Response("Please verify your email in order to suggest", 403)
    return Response("Due to bad feedback on your suggestions and votes, tour user is currently unable to suggest new /"
                    "translations", 403)
