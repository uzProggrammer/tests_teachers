from django.urls import path
from .views import (
    get_all_view,
    masala_view,
    like_toggle_view,
    get_masala_urinishlar_view,
    rating,
    masala_qoshish,
    masalaemas_view,
    testcases,
    testcases_post_view,
    to_archive,
    add_yechim_view,
    yechim_view,
    edit_testcase_view,
    get_all_view1,
    masala_tahrirla_view,
)

urlpatterns = [
    path('', get_all_view),
    path('add/', masala_qoshish),
    path('problem/<slug:slug>/', masala_view),
    path('problem/<slug:slug>/like-toggle/', like_toggle_view),
    path('problem/<slug:slug>/attempts/', get_masala_urinishlar_view),
    
    path('problem/<slug:slug>/rating/time/<str:type1>/', rating),
    path('problem/<slug:slug>/rating/<str:type1>/', rating),
    path('problem/<slug:slug>/rating/len/<str:type1>/', rating),
    path('problem/<slug:slug>/testcases', testcases),
    path('problem/<slug:slug>/testcasespost/', testcases_post_view),
    path('problem/<slug:slug>/testcase/edit/', edit_testcase_view),
    path('problem/<slug:slug>/add-solve/', add_yechim_view),
    path('problem/<slug:slug>/solve/', yechim_view),
    path('problem/<slug:slug>/edit/', masala_tahrirla_view),
    

    path('unproblem/<slug:slug>/rating/time/<str:type1>/', rating),
    path('unproblem/<slug:slug>/rating/<str:type1>/', rating),
    path('unproblem/<slug:slug>/rating/len/<str:type1>/', rating),
    path('unproblem/<slug:slug>/testcases', testcases),
    path('unproblem/<slug:slug>/', masalaemas_view),
    path('unproblem/<slug:slug>/attempts/', get_masala_urinishlar_view),
    path('unproblem/<slug:slug>/testcasespost/', testcases_post_view),
    path('unproblem/<slug:slug>/to-archive/', to_archive),
    path('unproblem/<slug:slug>/add-solve/', add_yechim_view),
    path('unproblem/<slug:slug>/solve/', yechim_view),
    path('unproblem/<slug:slug>/testcase/edit/', edit_testcase_view),
    path('unproblem/<slug:slug>/edit/', masala_tahrirla_view),
]