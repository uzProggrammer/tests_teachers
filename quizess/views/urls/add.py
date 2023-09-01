from django.urls import path
from quizess.views.add import add_quiz,add_test_view

urlpatterns = [
    path('add/', add_quiz),
    path('test/<int:id>/add-quiz/',add_test_view)
]