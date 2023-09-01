from django.urls import path
from .views import (
    get_masala_urinishlar_view,
    urinishlar_view,
    urinish_view,
    get_urinish_type
)

urlpatterns = [
    path('', urinishlar_view),
    path('attempt/<int:id>/', urinish_view),
    path('attempt/<int:id>/get-type/', get_urinish_type),
]