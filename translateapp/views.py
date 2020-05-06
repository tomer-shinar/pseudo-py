import os

from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
import Model
from rest_framework.response import Response
import json


@api_view(['POST'])
def translate(request):
    translator = Model.translate.TranslationModeBuilder().load(os.path.join("saved-files"))
    translation = translator.evaluate(request.data["pseudo"])
    return Response(json.dumps(translation))
