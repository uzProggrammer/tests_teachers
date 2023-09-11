from django.urls import path
from olimpiads.views import all_view, get_sol_view, get_problem_view, add_view, edit_view, add_solution1_view, edit2_view

urlpatterns = [
    path('', all_view),
    path('solution/<int:id>/', get_sol_view),
    path('solution/<int:id>/problem/<int:id1>/', get_problem_view),
    path('solution/<int:id>/problem/<int:id1>/edit/', edit2_view),
    path('solution/<int:id>/edit/', edit_view),
    path('solution/<int:id>/add-problem/', add_solution1_view),
    path('add/', add_view),
]