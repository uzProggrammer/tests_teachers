from django.urls import path
from .views import all_posts, post, update_post, create_post, delete_post, add_post_like

urlpatterns = [
    path('', all_posts, name='all_posts'),
    path('post/<int:post_id>', post, name='post'),
    path('post/<int:post_id>/edit/', update_post, name='post_edit'),
    path('add/', create_post, name='add_post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('post/<int:post_id>/like/', add_post_like, name='add_post_like')
]