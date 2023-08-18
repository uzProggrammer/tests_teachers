from django.urls import path
from .views import task_detail, add_tasks, edit_task, tasks

urlpatterns = [
    path('problem/<int:task_id>/', task_detail, name='problem_detail'),
    path('add/', add_tasks, name='add_task'),
    path('problem/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('', tasks, name='problems'),
]