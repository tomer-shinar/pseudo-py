from django.urls import path
from translateapp import views

urlpatterns = [
    path('translate', views.translate, name='translate'),
]