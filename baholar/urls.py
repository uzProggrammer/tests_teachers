from django.urls import path
from .views import baho, assignment_baho, bsb_ball

urlpatterns = [
    path('profile/<str:username>/price/', baho, name='baho'),
    path('profile/<str:username>/prices/assignment/', assignment_baho, name='assignment_baho'),
    path('profile/<str:username>/prices/controls/', bsb_ball, name='bsb_ball_user')
]