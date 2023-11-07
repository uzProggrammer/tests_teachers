from django.urls import path, include
from .views import login_api

urlpatterns = [
    path('login/', login_api),
]