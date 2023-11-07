from django.urls import path, include


urlpatterns = [
    path('users/', include('apiv1.users.urls')),
    path('chats/', include('apiv1.chats.urls')),
]