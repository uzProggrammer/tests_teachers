from django.urls import path
from .creates import create_course, create_lesson, url_to_create, create_quiz_view, create_multiquiz_view, create_lecture_view, \
    create_closedtest_view, create_drag_and_drop_view

urlpatterns = [
    path('add/', create_course),
    path('course/<int:id>/lesson-add/', create_lesson),
    path('course/<id>/lesson/<slug>/add-item', url_to_create),
    path('course/<id>/lesson/<slug>/add-test/', create_quiz_view),
    path('course/<id>/lesson/<slug>/add-multi-test/', create_multiquiz_view),
    path('course/<id>/lesson/<slug>/add-lecture/', create_lecture_view),
    path('course/<id>/lesson/<slug>/add-closed-test/', create_closedtest_view),
    path('course/<id>/lesson/<slug>/add-drag-and-drop-test/', create_drag_and_drop_view),
]