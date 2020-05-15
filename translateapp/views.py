import os
from rest_framework.decorators import api_view
import Model
from rest_framework.response import Response
import json
from .serializers import *
from rest_framework.views import APIView
from rest_framework import permissions, status


@api_view(['POST'])
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
