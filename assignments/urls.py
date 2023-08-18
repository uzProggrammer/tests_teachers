from django.urls import path
from .views import (
    all_assignments,
    assignment_view,
    add_comment_like,
    add_answer_like,
    add_assignment,
    edit,

)

urlpatterns = [
    path('', all_assignments, name='assignments'),
    path('assignment/<int:id>/', assignment_view, name='assignment'),
    path('like_comment/<int:id>/', add_comment_like, name='add_comment_like'),
    path('like_answer/<int:id>/', add_answer_like, name='add_answer_like'),
    path('add/', add_assignment, name='add_assignment'),
    path('assignment/<int:id>/edit/', edit, name='assignment_edit'),
]