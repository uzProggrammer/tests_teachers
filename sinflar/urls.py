from django.urls import path

from .views import sinflar_view, sinf, add_student, edit_class_view, remove_student, sinf_student

urlpatterns = [
    path('', sinflar_view, name='all_sinflar'),
    path('class/<slug:slug>/', sinf, name="sinf"),
    path('class/<slug:slug>/add_student/', add_student, name='add_student_sinf'),
    path('class/<slug:slug>/edit_class/', edit_class_view, name="edit_sinf"),
    path('class/<slug:slug>/remove_student/', remove_student, name="remove_student"),
    path('class/<slug:slug>/student/<str:username>/', sinf_student, name="sinf_student"),
]