"""tests_teachers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from bsb.models import BSB
from posts.models import Post
from problems.models import Problem
from users.models import MyUser
from quizess.models import Task
from assignments.models import Assignment, StudentAnswer
from django.conf.urls.static import static
from searchs.views import permission_denied, server_error, bad_request

def home(request):
    unread_assign = None
    unread_answerca2 = []
    if request.user.is_authenticated:
        unread_assign = Assignment.objects.filter(is_readed=False, student=request.user)

        unread_answerca = StudentAnswer.objects.filter(is_readed=False)
        unread_answerca2 = []
        for unread_answerca1 in unread_answerca:

            if unread_answerca1.assignment.author == request.user:
                a = unread_answerca1
                unread_answerca2.append(a)
    users = MyUser.objects.all()
    tasks = Task.objects.all()
    posts = Post.objects.all()
    controls = BSB.objects.all().count()
    assignments = Assignment.objects.count()
    problems = Problem.objects.count()
    return render(request, 'home.html', {'users': users, 'tasks': tasks, 'posts': posts, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2), 'controls': controls, 'assignments': assignments, 'problems': problems})

def notFound(request, exception):
    unread_assign = None
    unread_answerca2 = []
    if request.user.is_authenticated:
        unread_assign = Assignment.objects.filter(is_readed=False, student=request.user)

        unread_answerca = StudentAnswer.objects.filter(is_readed=False)
        unread_answerca2 = []
        for unread_answerca1 in unread_answerca:

            if unread_answerca1.assignment.author == request.user:
                a = unread_answerca1
                unread_answerca2.append(a)
    return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})



urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('', home, name='home'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('posts/', include('posts.urls')),
    path('tests/', include('quizess.urls')),
    path('', include('searchs.urls')),
    path('404/', notFound, name='notFound'),
    path('informatics/', include('infotmatika.urls')),
    path('assignments/', include('assignments.urls')),
    path('chats/', include('my_messages.urls')),
    path('classes/', include('sinflar.urls')),
    path('controls/', include('bsb.urls')),
    path('users/', include('baholar.urls')),
    path('courses/', include('courses.urls')),
    path('courses/', include('courses.creates_url')),
    path('courses/', include('courses.edits_url')),
]

handler404 = notFound
handler403 = permission_denied
handler400 = bad_request
handler500 = server_error