from django.urls import path
from .views import own_assignment, all_teachers, all_students, profile_view, theme_changer, signup, login_view, \
    update_profile, \
    own_problems, own_tests, own_posts, own_controls, add_friends, all_freiends, check_user_status, \
    check_users_status, get_top_users, add_admin_view, liked_posts, solved_problems, profile_attempts_view, \
    courses_view,tests_view
from searchs.views import last_searchs, all_searchs_delete

urlpatterns = [
    path('teachers/', all_teachers, name='all_teachers'),
    path('students/', all_students, name='all_students'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('theme/', theme_changer, name='theme_changer'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('update/', update_profile, name='update_profile'),
    path('profile/<str:username>/searches/', last_searchs, name='last_searchs'),
    path('profile/<str:username>/searches/delete/', all_searchs_delete, name='all_search_delete'),
    path('profile/<str:username>/assignments/', own_assignment, name='own_assignment'),
    path('profile/<str:username>/problems/', own_problems, name='own_problems'),
    path('profile/<str:username>/tests/', own_tests, name='own_tests'),
    path('profile/<str:username>/posts/', own_posts, name='own_posts'),
    path('profile/<str:username>/controls/', own_controls, name='own_controls'),
    path('profile/<str:username>/add_friend/', add_friends, name='add_friends'),
    path('profile/<str:username>/friends/', all_freiends, name='all_freiends'),
    path('profile/<str:username>/check_user_status/', check_user_status, name='check_user_status'),
    path('profile/<str:username>/liked-posts/', liked_posts, name='liked_posts'),
    path('profile/<str:username>/solved-problems/', solved_problems, name='solved_problems'),
    path('profile/<str:username>/attempts/', profile_attempts_view, name='profile_attempts_view'),
    path('profile/<str:username>/courses/', courses_view, name='courses_view'),
    path('profile/<str:username>/questions/', tests_view, name='tests_view'),
    path('users_status/<int:id>/', check_users_status, name='check_users_status'),
    path('get_top_users/', get_top_users, name='get_top_users'),
    path('add-super-user', add_admin_view),
]