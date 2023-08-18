from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import MyUser
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegisterForm, UserProfile
from quizess.models import Result
from assignments.models import Assignment, StudentAnswer
from sinflar.models import Sinf
import random
import string
from django.db.models import Q

def all_teachers(request,):
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
    teachers = MyUser.objects.filter(is_teacher=True)
    return render(request, 'users/all.html', {'teachers': teachers, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def all_students(request,):
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
    students = MyUser.objects.filter(is_teacher=False)

    return render(request, 'users/all_students.html', {'students': students, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def profile_view(request, username):
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
    profile = get_object_or_404(MyUser, username=username)
    test = 0
    try:
        res = Result.objects.filter(user=profile)
        test+=res.count()
    except Result.DoesNotExists:
        pass
    return render(request, 'users/profile.html', {'profile':profile, 'test': test, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def theme_changer(request):
    profile = MyUser.objects.get(username=request.user.username)
    if profile.theme == 'default':
        profile.theme = 'light'
        profile.save()
    else:
        profile.theme = 'default'
        profile.save()
    return HttpResponseRedirect('/')

def signup(request):
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
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Muvoffiqiyatli ro\'yxatdan o\'tildi!')

            last = MyUser.objects.last()
            sinf, get = Sinf.objects.get_or_create(nom=last.sinf)
            if get == False:
                sinf.students.add(last)
            else:
                letters = string.ascii_letters
                digits = string.digits
                all_ch = letters + digits
                pwd_length = 40
                sinf.students.add(last)
                pwd = ''.join(random.sample(all_ch, pwd_length))
                sinf.url = pwd
                sinf.active_user = last
                sinf.author_student = last
            sinf.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/signup.html', {'form': form, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def login_view(request):
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Muvoffiqiyatli tizimga kirdingiz!')
            return redirect('home')
        else:
            messages.error(request, 'Bunday foydalanuvchi tizimda topilmadi. Hohlasangiz ro\'yxatdan o\'ting: <a href="/users/signup">Ro\'yxatdan o\'tish</a>')
    return render(request, 'users/login.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def update_profile(request):
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
    if request.user.is_authenticated:
        profile = request.user
        form = UserProfile(request.POST or None, instance=profile)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Muvoffiqiyatli profilingiz tahrirlandi! ')
                return HttpResponseRedirect(f'/users/profile/{profile.username}/')
        return render(request, 'users/update_profile.html', {'form': form, 'profile': profile, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    else:
        return render(request, '404.html',{'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def own_assignment(request, username):
    if request.user.is_authenticated:
        profile = get_object_or_404(MyUser, username=username)
        search = ''
        if profile.is_staff or profile.is_teacher:
            assignments = profile.assignment_author.all()
            if 'search' in request.GET:
                search = request.GET.get('search')
                assignments = profile.assignment_author.filter(
                    Q(title__icontains=request.GET.get('search')) | Q(info__icontains=request.GET.get('search'))
                )
                if 'answers_count' in request.GET:
                    if request.GET.get('answers_count') != 'all':
                        assignments = assignments.filter(assigment_answer=request.GET.get('answers_count'))
            if 'answers_count' in request.GET:
                if request.GET.get('answers_count') != 'all':
                    assignments = assignments.filter(assigment_answer=request.GET.get('answers_count'))
            object = Paginator(assignments, 40)
            if 'page' in request.GET:
                object.page(request.GET['page'])
            else:
                object.page(1)
            return render(request, 'users/own_assignments.html', {'profile': profile, 'object':object, 'search': search})
        else:
            return render(request, '404.html')
    else:
        return HttpResponseRedirect('/users/login/')

def own_problems(request, username):
    if request.user.is_authenticated:
        profile = get_object_or_404(MyUser, username=username)
        problems = profile.user_task.all()
        if 'search' in request.GET:
            search = request.GET.get('search')
            problems = profile.user_task.filter(
                Q(title__icontains=request.GET.get('search')) | Q(about__icontains=request.GET.get('search'))
            )
        object = Paginator(problems, 40)
        if 'page' in request.GET:
            object.page(request.GET['page'])
        else:
            object.page(1)
        return render(request, 'users/own_problems.html', {'profile': profile, 'object': object})
    else:
        return HttpResponseRedirect('/users/login/')

def own_tests(request, username):
    if request.user.is_authenticated:
        profile = get_object_or_404(MyUser, username=username)
        tests = profile.author_test.all()
        if 'search' in request.GET:
            tests = profile.author_test.filter(
                Q(title__icontains=request.GET.get('search')) | Q(about__icontains=request.GET.get('search'))
            )

        object = Paginator(tests, 40)
        if 'page' in request.GET:
            object.page(request.GET['page'])
        else:
            object.page(1)
        return render(request, 'users/own_tests.html', {'profile':profile, 'object':object})
    else:
        return HttpResponseRedirect('users/login/')

def own_posts(request, username):
    if request.user.is_authenticated:
        profile = get_object_or_404(MyUser, username=username)
        tests = profile.user_post.all()
        if 'search' in request.GET:
            tests = profile.user_post.filter(
                Q(title__icontains=request.GET.get('search')) | Q(content__icontains=request.GET.get('search'))
            )

        object = Paginator(tests, 40)
        if 'page' in request.GET:
            object.page(request.GET['page'])
        else:
            object.page(1)
        return render(request, 'users/own_posts.html', {'profile':profile, 'object':object})
    else:
        return HttpResponseRedirect('users/login/')

def own_controls(request, username):
    if request.user.is_authenticated:
        profile = get_object_or_404(MyUser, username=username)
        controls = profile.author_BSB.all()
        if 'type' in request.GET:
            if request.GET.get('type') != 'all':
                controls = profile.author_BSB.filter(
                    type=request.GET.get('type')
                )
        if 'search' in request.GET:
            controls = profile.author_BSB.filter(
                Q(title__icontains=request.GET.get('search'))
            )
            if 'type' in request.GET:
                if request.GET.get('type') != 'all':
                    controls = profile.author_BSB.filter(
                        type=request.GET.get('type')
                    )

        object = Paginator(controls, 40)
        if 'page' in request.GET:
            object.page(request.GET['page'])
        else:
            object.page(1)
        return render(request, 'users/own_controls.html', {'profile':profile, 'object':object})
    else:
        return HttpResponseRedirect('users/login/')

def add_friends(request, username):
    if request.user.is_authenticated:
        user = MyUser.objects.get(username=username)
        user1 = MyUser.objects.get(username=request.user.username)
        if not user in user1.friends.all():
            user1.friends.add(user)
        else:
            user1.friends.remove(user)
        user1.save()
        return HttpResponseRedirect(f'/users/profile/{username}/')
    else:
        return HttpResponseRedirect('/users/login')

def all_freiends(request, username):
    if request.user.is_authenticated:
        profile = MyUser.objects.get(username=username)
        friends = profile.friends.all()

        if 'sinf' in request.GET:
            if request.GET.get('sinf') != 'all':
                friends = profile.friends.filter(
                    sinf=request.GET.get('sinf')
                )
        if 'search' in request.GET:
            friends = profile.friends.filter(
                Q(username__icontains=request.GET.get('search')) | Q(first_name__icontains=request.GET.get('search')) | Q(last_name__icontains=request.GET.get('search')) | Q(email__icontains=request.GET.get('search'))
            )
            if 'sinf' in request.GET:
                if request.GET.get('sinf') != 'all':
                    friends = profile.friends.filter(
                        sinf=request.GET.get('sinf')
                    )

        object = Paginator(friends, 20)
        if 'page' in request.GET:
            object.page(request.GET['page'])
        else:
            object.page(1)
        return render(request,  'users/all_friends.html', {'profile':profile, 'object':object})
    else:
        return HttpResponseRedirect('/users/login/')

from datetime import timedelta
from django.contrib.humanize.templatetags.humanize import naturaltime
def check_user_status(request, username):
    user = get_object_or_404(MyUser, username=username)
    now = timezone.now()
    now_10 = now - timedelta(minutes = 1)
    try:

        if now_10 < user.last_visit < now:
            return JsonResponse({'is_online': True})
    except:
        user.last_visit=user.date_joined
        user.save()
    return JsonResponse({'is_online': False, 'time': naturaltime(user.last_visit)})

def check_users_status(request, id):
    users = Sinf.objects.get(id=id).students.all()
    now = timezone.now()
    now_10 = now - timedelta(minutes = 1)
    data1 = {}
    data = {}
    for user in users:
        try:
            if now_10 < user.last_visit < now:
                data[user.username] = {'is_online': True, 'full': user.last_name+' '+user.first_name}
            else:
                pass
        except:
            pass
    return JsonResponse(data)


from django.core import serializers
def get_top_users(request):
    try:
        users = MyUser.objects.all().order_by('-ball')[:5]
        data = {}
        for user in users:
            data[f'{user.username}']={
                'username': user.username,
                'full': user.last_name+' '+ user.first_name,
                'ball': user.ball
            }
        return JsonResponse(data)
    except IndexError:
        users = MyUser.objects.all().order_by('-ball')
        data = {}
        for user in users:
            data[f'{user.username}'] = {
                'username': user.username,
                'full': user.last_name + ' ' + user.first_name,
                'ball': user.ball
            }
        return JsonResponse(data)