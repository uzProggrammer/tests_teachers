from django.urls import *

from .edits_view import (
    edit_course_view,
    edit_lesson_view,
    edit_lecture_view,
    edit_drag_and_drop_view,
    edit_closedtest_view,
    edit_multiquiz_view,
    edit_quiz_view,
)

urlpatterns = [
    path('course/<int:id>/edit/', edit_course_view),
    path('course/<int:id>/lesson/<slug:slug>/edit/', edit_lesson_view),
    path('course/<int:id>/lesson/<slug:slug>/lecture/<slug:slug1>/edit/', edit_lecture_view),
    path('course/<int:id>/lesson/<slug:slug>/drag-and-drop/<slug:slug1>/edit/', edit_drag_and_drop_view),
    path('course/<int:id>/lesson/<slug:slug>/closed-test/<slug:slug1>/edit/', edit_closedtest_view),
    path('course/<int:id>/lesson/<slug:slug>/multi-quiz/<slug:slug1>/edit/', edit_multiquiz_view),
    path('course/<int:id>/lesson/<slug:slug>/quiz/<slug:slug1>/edit/', edit_quiz_view),
]