from django.urls import path
from .views import (
    all_bsb,
    bsb_view,
    bsb_assignments,
    bsb_assignment,
    add_bsb_assignment, edit_bsb_assignment, edit_bsb, add_bsb, results, add_answer_ball,
    bsb_problems, bsb_problem, edit_bsb_problem, get_attempt, add_bsb_problem, bsb_quizess, post_bsb_question,
    add_bsb_quiz, quiz_answer,
    clone_bsb,delete_bsb
)
urlpatterns = [
    path('', all_bsb, name='all_bsb'),
    path('control/<int:id>/', bsb_view, name='bsb'),
    path('control/<int:id>/assignments/', bsb_assignments, name='bsb_assignments'),
    path('control/<int:id>/assignments/assignment/<int:id1>/', bsb_assignment, name='bsb_assignment'),
    path('control/<int:id>/assignments/add/', add_bsb_assignment, name='add_bsb_assignment'),
    path('control/<int:id>/assignments/assignment/<int:id1>/edit/', edit_bsb_assignment, name='edit_bsb_assignment'),
    path('control/<int:id>/edit/', edit_bsb, name='bsb_edit'),
    path('control/<int:id>/clone/', clone_bsb, name='clone_bsb'),
    path('control/<int:id>/delete/', delete_bsb, name='delete_bsb'),
    path('create/', add_bsb, name='add_bsb'),
    path('control/<int:id>/results/', results, name='bsb_results'),
    path('control/<int:id>/student/answer/<int:id1>/', add_answer_ball, name='bsb_student_answer'),
    path('control/<int:id>/problems/', bsb_problems, name='bsb_problems'),
    path('control/<int:id>/problems/problem/<int:id1>/', bsb_problem, name='bsb_problem'),
    path('control/<int:id>/problems/problem/<int:id1>/edit/', edit_bsb_problem, name='edit_bsb_problem'),
    path('control/<int:id>/attempts/attempt/<int:id1>/', get_attempt, name='bsb_attempt'),
    path('control/<int:id>/problems/add/', add_bsb_problem, name="add_bsb_problem"),
    path('control/<int:id>/tests/', bsb_quizess, name="bsb_tests"),
    path('control/<int:id>/tests/post/', post_bsb_question, name='bsb_quiz_post'),
    path('control/<int:id>/tests/add/', add_bsb_quiz, name='add_bsb_quiz'),
    path('control/<int:id>/tests/answer/<int:id1>/', quiz_answer, name='bsb_quiz_answer')
]