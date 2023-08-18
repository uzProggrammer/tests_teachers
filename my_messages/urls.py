from django.urls import path
from .views import (
    all_chats,
    user_chat,
    create_message,
    get_unread_message,
    delete_message,
    update_message,
    change_notification,
    create_chat,
    get_users_for_new_chat,
    get_users_1
)

urlpatterns = [
    path('', all_chats, name='all_chats'),
    path('with/<str:recipient>/', user_chat, name='user_chat'),
    path('with/<str:recipient>/add_message/', create_message, name='create_message'),
    path('with/<str:recipient>/get_unread_message/', get_unread_message, name='get_unread_message'),
    path('with/<str:recipient>/delete_message/', delete_message, name='delete_message'),
    path('with/<str:recipient>/update_message/', update_message, name='update_message'),
    path('with/<str:recipient>/change_notification/', change_notification, name="change_notification"),
    path('with/<str:recipient>/create/', create_chat, name="create_chat"),
    path('users/', get_users_for_new_chat, name='users_for_chat'),
]