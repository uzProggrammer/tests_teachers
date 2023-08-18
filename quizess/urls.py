from django.urls import path
from .views import all_tests, test_detail, questions, questions_post, add_test, test_add_1, actived_test, edit_test, reuslt

urlpatterns = [
    path('', all_tests, name='all_tests'),
    path('test/<int:id>/', test_detail, name='test_detail'),
    path('test/<int:id>/questions/', questions, name='questions'),
    path('test/<int:id>/questions/post/', questions_post, name='questions_post'),
    path('add/', add_test, name='add_test'),
    path('test/<int:id>/add/question/', test_add_1, name='add_test_question'),
    path('test/<int:id>/print/', actived_test, name='actived_test'),
    path('test/<int:id>/edit/', edit_test, name='edit_test'),
    path('test/<int:id>/results/', reuslt, name="test_results")
]