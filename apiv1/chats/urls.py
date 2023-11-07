from django.urls import path

from apiv1.chats.views import (
    all_chats,
    user_chat,
    get_search_users,
    start_chat,
    create_message,
    delete_message,
    delete_chat,
)

urlpatterns = [
    path('<str:auth_token>/', all_chats),
    path('<str:auth_token>/<int:id1>/', user_chat),
    path('<str:auth_token>/search', get_search_users),
    path('<str:auth_token>/create/<int:res_id>/', start_chat),
    path('<str:auth_token>/<int:id>/send', create_message),
    path('<str:auth_token>/<int:id>/delete-m/<int:id1>', delete_message),
    path('<str:auth_token>/<int:id>/delete/', delete_chat),
]