from quizess.views.detail import (
    all_view,
    deteil_view,
    start_test_view,
    quizes_view,
    quizes_post_view,
    get_started_time_api,
    public_api,
    results_view,
    result_view,
    result1_view,
    delete_test,
)
from django.urls import path

urlpatterns = [
    path('', all_view),
    path('test/<int:id>/', deteil_view),
    path('test/<int:id>/delete/', delete_test),
    path('test/<int:id>/start/', start_test_view),
    path('test/<id>/quizes/', quizes_view),
    path('test/<int:id>/quizes/post/', quizes_post_view),
    path('test/<int:id>/quizes/get-time/', get_started_time_api),
    path('test/<int:id>/results/', results_view),
    path('test/<int:id>/public/', public_api),
    path('test/<int:id>/result/', result_view),
    path('test/<int:id>/result/<int:id1>/', result1_view),
]