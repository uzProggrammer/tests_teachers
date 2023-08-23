from django.urls import path
from .views import (
    get_masala_urinishlar_view,
    urinishlar_view,
    urinish_view,
)

urlpatterns = [
    path('', urinishlar_view),
    path('attempt/<int:id>/', urinish_view)
]