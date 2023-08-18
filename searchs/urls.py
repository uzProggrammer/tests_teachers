from django.urls import path
from .views import search, theme_light, theme_blue, nav_blue, nav_brown, nav_black,nav_green,nav_light,theme_black, \
    theme_green, theme_brown, edit_font, notification

urlpatterns = [
    path('search/', search, name='search'),
    path('theme/light/', theme_light, name='theme_light'),
    path('theme/blue/', theme_blue, name='theme_blue'),
    path('nav/blue/', nav_blue, name='nav_blue'),
    path('nav/brown/', nav_brown, name='nav_brown'),
    path('nav/black/', nav_black, name='nav_black'),
    path('nav/green/', nav_green, name='nav_green'),
    path('nav/light/', nav_light, name='nav_light'),
    path('theme/black/', theme_black, name='theme_black'),
    path('theme/green/', theme_green, name='theme_green'),
    path('theme/brown/', theme_brown, name='theme_brown'),
    path('font/', edit_font, name='edit_font'),
    path('notification/', notification, name='notification')
]