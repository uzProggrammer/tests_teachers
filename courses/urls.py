from django.urls import *

from .views import (
    all_lessons_view,
    get_course_view,
    start_course_view,
    lesson_view,
    get_lessens_view,
    lecture_view,
    quiz_view,
    closed_quiz_view,
    drag_and_drop,
    drag_and_drop_post,
    get_multi_quiz_view,
)

urlpatterns = [
    path('', all_lessons_view),
    path('course/<int:id>/', get_course_view),
    path('course/<int:course_id>/start/', start_course_view),
    path('course/<int:id>/lesson/<slug:slug>/', lesson_view),
    path('course/<int:id>/get-lessons/', get_lessens_view),
    path('course/<int:id>/lesson/<slug:slug>/lecture/<slug:slug1>/', lecture_view),
    
    path('course/<int:id>/lesson/<slug:slug>/quiz/<slug:slug1>/', quiz_view),
    path('course/<int:id>/lesson/<slug:slug>/closed-test/<slug:slug1>/', closed_quiz_view),
    path('course/<int:id>/lesson/<slug:slug>/drag-and-drop/<slug:slug1>/', drag_and_drop),
    path('course/<int:id>/lesson/<slug:slug>/drag-and-drop/<slug:slug1>/post/', drag_and_drop_post),
    path('course/<int:id>/lesson/<slug:slug>/multi-quiz/<slug:slug1>/', get_multi_quiz_view),
]