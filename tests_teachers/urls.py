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
from django.http import JsonResponse
from django.urls import path, include
from django.shortcuts import render

from bsb.models import BSB
from posts.models import Post
from users.models import MyUser
from assignments.models import Assignment, StudentAnswer
from django.conf.urls.static import static
from searchs.views import permission_denied, server_error, bad_request
from quizess.models import Quiz
from Masalalar.models import Masala
from assignments.models import Assignment
from courses.models import Course


def home(request):
    return render(request, 'home.html')

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

def get_counts_api(reqeust):
    data={}
    a = MyUser.objects.filter(is_teacher=True).count()
    data['t']=a
    b = MyUser.objects.filter(is_teacher=False).count()
    data['s']=b
    c=Quiz.objects.all().count()
    data['q']=c
    d = Masala.objects.all().count()
    data['m']=d
    f = BSB.objects.count()
    data['c']=f
    j = Assignment.objects.count()
    data['a'] = j
    data['c1'] = Course.objects.count()
    return JsonResponse(data)

def get_api_2(reqeust):
    courses = Course.objects.all().order_by('users')[:8]
    data = {}
    for i in courses:
        data1 = {
            'title': i.title,
            'id': i.id,
            'about': i.summary,
            'users': i.users.count(),
            'teg': i.tags.all()[0].title if i.tags else ''
        }
        data[i.id] = data1
    return JsonResponse(data)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('', home, name='home'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('tests/', include('quizess.views.urls.add')),
    path('tests/', include('quizess.views.urls.detail')),
    path('tests/', include('quizess.views.urls.edit')),
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
    path('olympiad-solutions/', include('olimpiads.urls')),
    path('api1/', get_counts_api),
    path('api2/', get_api_2),
]

handler404 = notFound
handler403 = permission_denied
handler400 = bad_request
handler500 = server_error