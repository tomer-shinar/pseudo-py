from django.urls import path
from translateapp import views

urlpatterns = [
    path('translate', views.translate, name='translate'),
    path('current_user/', views.current_user),
    path('users/', views.UserList.as_view())
]