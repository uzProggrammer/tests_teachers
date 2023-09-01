from django.urls import path
from quizess.views.edit import edit_quiz_view

urlpatterns= [
    path('test/<int:id>/edit/', edit_quiz_view)
]