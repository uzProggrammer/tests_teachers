from django.urls import path, include

from .views import info

urlpatterns = [
    path('info/', info, name='informatics_info'),
    path('problems/', include('problems.urls')),
    path('attempts/', include('attempts.urls')),
]