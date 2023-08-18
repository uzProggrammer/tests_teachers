import string

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from users.models import MyUser
from .models import Sinf
import random

def sinflar_view(request):
    sinflar = Sinf.objects.all().order_by('-ball')
    return render(request, 'sinflar/all.html', {'sinflar': sinflar})

def sinf(request, slug):
    sinf = get_object_or_404(Sinf, url=slug)
    students = sinf.students.all().order_by('username')
    studentca = sinf.students.all().order_by('-ball')[0]
    studentca1 = sinf.students.all().order_by('ball', 'date_joined')[0]
    ballar = 0
    for user in students:
        ballar += user.ball
    new_ball = ballar - sinf.ball
    sinf.ball += new_ball
    sinf.active_user = studentca
    sinf.save()
    return render(request, 'sinflar/sinf.html', {'sinf':sinf, 'students': students, 'studentca1':studentca1})

def add_student(request, slug):
    sinf = get_object_or_404(Sinf, url=slug)
    users = MyUser.objects.filter(is_student=True, is_teacher=False)

    if request.method=='POST':
        if request.user.is_authenticated and request.user.is_teacher or request.user == sinf.author_student or request.user.is_staff:
            helper_users = request.POST.getlist('helper_users')
            for helper_user in helper_users:
                user = MyUser.objects.get(id=helper_user)
                if user in sinf.students.all():
                    pass
                else:
                    sinf.students.add(user)
                    sinf.ball += user.ball
                    sinf.save()
            sinf.save()
            return HttpResponseRedirect(f'/classes/class/{sinf.url}/')
        else:
            return HttpResponseRedirect('users/login/')
    return render(request, 'sinflar/add_student.html', {'sinf':sinf,'users':users})

def edit_class_view(request, slug):
    sinf = get_object_or_404(Sinf, url=slug)
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_teacher or request.user == sinf.author_student or request.user.is_staff:
            name_class = request.POST.get('name_class', False)
            students_count = request.POST.get('students_count', False)
            sinf.nom = name_class
            sinf.max_students = students_count
            letters = string.ascii_letters
            digits = string.digits
            all_ch = letters+digits
            pwd_length = 40
            pwd = ''.join(random.sample(all_ch, pwd_length))
            sinf.url = pwd
            sinf.save()
            return HttpResponseRedirect(f'/classes/class/{sinf.url}')
        else:
            return HttpResponseRedirect('users/login/')
    return render(request, 'sinflar/edit_class.html', {'sinf': sinf})

def remove_student(request, slug):
    sinf = get_object_or_404(Sinf, url=slug)
    users = sinf.students.all()
    if request.method=='POST':
        if request.user.is_authenticated and request.user.is_teacher or request.user == sinf.author_student or request.user.is_staff:
            helper_users = request.POST.getlist('helper_users')
            for helper_user in helper_users:
                user = MyUser.objects.get(id=helper_user)
                sinf.students.remove(user)
                sinf.ball -= user.ball
                sinf.save()
            sinf.save()
            return HttpResponseRedirect(f'/classes/class/{sinf.url}/')
        else:
            return HttpResponseRedirect('users/login/')
    return render(request, 'sinflar/remove_student.html', {'sinf':sinf,'users':users})

def sinf_student(request, slug, username):
    profile = get_object_or_404(MyUser, username=username)
    return render(request, 'users/profile.html', {'profile': profile})