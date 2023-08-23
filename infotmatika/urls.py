from django.urls import path, include

from .views import info
from Masalalar.views import get_all_view1

urlpatterns = [
    path('info/', info, name='informatics_info'),
    path('problems/', include('Masalalar.urls')),
    path('attempts/', include('Masalalar.urinishlar')),
    path('unproblems/', get_all_view1),
]