from django.urls import path
from .views import all_attempts, attempt_detail

urlpatterns = [
    path('', all_attempts, name='all_attempts'),
    path('attempt/<int:id>/', attempt_detail, name='attempt_detail'),
]