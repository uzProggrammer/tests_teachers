from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.utils import timezone

from Masalalar.models import Masala, Urinish

from .models import MyUser
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegisterForm, UserProfile
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
            messages.success(request, 'Muvaffaqiyatli tizimga kirdingiz!')
            return redirect('home')
        else:
            messages.error(request, 'Bunday foydalanuvchi tizimda topilmadi. Hohlasangiz ro\'yxatdan o\'ting: <a href="/users/signup">Ro\'yxatdan o\'tish</a>')

        return HttpResponseRedirect(f'/users/login/')
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
            assignments = Paginator(assignments, 40)
            if 'page' in request.GET:
                object = assignments.page(request.GET['page'])
            else:
                object=assignments.page(1)
            return render(request, 'users/own_assignments.html', {'profile': profile, 'page_obj':object,'object':assignments, 'search': search})
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
        search = ''
        if 'search' in request.GET:
            search=request.GET.get('search')
            controls = profile.author_BSB.filter(
                Q(title__icontains=search) | Q(sinf__nom__icontains=search)
            )
            if 'type' in request.GET:
                if request.GET.get('type') != 'all':
                    controls = profile.author_BSB.filter(
                        type=request.GET.get('type')
                    )

        controls = Paginator(controls, 5)
        if 'page' in request.GET:
            object = controls.page(request.GET['page'])
        else:
            object = controls.page(1)
        return render(request, 'users/own_controls.html', {'profile':profile, 'object':controls, 'page_obj':object, 'search':search})
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
    return JsonResponse({'is_online': False, 'time': user.status()})

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

def add_admin_view(request, type=None):
    if request.user.is_authenticated:
        if request.user.is_staff:
            username = ''
            is_staff = False
            if request.method == 'POST':
                username = request.POST.get('username')
                if 'is_staff' in request.POST:
                    is_staff=True
                user = get_object_or_404(MyUser, username=username)
                user.is_staff = is_staff
                user.is_teacher = True

                user.save()
                messages.success(request, f'{user.username} muvoffiqiyatli o\'qituvchi qilib tayinlandi')
                return HttpResponseRedirect(f'/users/profile/{user.username}/')
            return render(request, 'users/add_super_user1.html', {'is_user': True})
        else:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()

def liked_posts(request, username):
    profile = get_object_or_404(MyUser, username=username)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == profile:
            posts = profile.post_likes.all()
            masalalar = Paginator(posts, 20)
            if 'page' in request.GET:
                object = masalalar.page(request.GET['page'])
            else:
                object = masalalar.page(1)
            return render(request, 'users/liked_posts.html', {'profile': profile, 'page_obj': object, 'object': masalalar,})
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '403.html', status=403)

def solved_problems(request, username):
    profile = get_object_or_404(MyUser, username=username)
    masalalar = profile.masala_accepts.all()

    seach = ''
    if 'q' in request.GET:
        search = request.GET.get('q')
        seach = search
        masalalar = Masala.objects.filter(Q(title__icontains=search) | Q(
            body__icontains=search) | Q(info_in__icontains=search) | Q(out__icontains=search))
    type1 = 0
    if 'type' in request.GET and request.user.is_authenticated:
        type1 = str(request.GET.get('type'))
        if type1.isdigit():
            type1 = int(type1)
            if type1 != 0:
                if type1 == 1:
                    masala_accepts = request.user.masala_wrongs.all()
                    masalalar = masala_accepts
                elif type1 == 2:
                    masalalar = request.user.masala_accepts.all()
                else:
                    masala_wrong = request.user.masala_wrongs.all()
                    masala_accpted = request.user.masala_accepts.all()
                    masalalar = masalalar ^ (masala_accpted | masala_wrong)
    masalalar = Paginator(masalalar, 20)


    if 'page' in request.GET:
        object = masalalar.page(request.GET['page'])
    else:
        object = masalalar.page(1)
    return render(request, 'users/solved_problems.html', {'profile': profile, 'page_obj': object, 'object': masalalar, 'search': seach, 'type': type1})

def profile_attempts_view(request, username):
    profile = get_object_or_404(MyUser, username=username)
    masalalar = Paginator(Urinish.objects.filter(user=profile).order_by('-id'), 30)
    if 'page' in request.GET:
        object = masalalar.page(request.GET['page'])
    else:
        object = masalalar.page(1)
    return render(request, 'users/attempts.html', {'profile': profile, 'object_list': object, 'object': masalalar})

def courses_view(request, username):
    profile = get_object_or_404(MyUser, username=username)
    if profile.is_staff or profile.is_teacher:
        courses = profile.courses.all()
        masalalar = Paginator(courses, 30)
        if 'page' in request.GET:
            object = masalalar.page(request.GET['page'])
        else:
            object = masalalar.page(1)
        return render(request, 'users/courses.html', {'profile': profile, 'object_list': object, 'object': masalalar})
    else:
        courses = profile.followed_courses.all()
        masalalar = Paginator(courses, 30)
        if 'page' in request.GET:
            object = masalalar.page(request.GET['page'])
        else:
            object = masalalar.page(1)
        return render(request, 'users/courses.html', {'profile': profile, 'object_list': object, 'object': masalalar})

def tests_view(request, username):
    profile = get_object_or_404(MyUser, username=username)
    if profile.is_staff or profile.is_teacher:
        courses = profile.author_test.all()
        masalalar = Paginator(courses, 30)
        if 'page' in request.GET:
            object = masalalar.page(request.GET['page'])
        else:
            object = masalalar.page(1)
        return render(request, 'users/quizess.html', {'profile': profile, 'object_list': object, 'object': masalalar})
    else:
        courses = profile.tasks.all()
        masalalar = Paginator(courses, 30)
        if 'page' in request.GET:
            object = masalalar.page(request.GET['page'])
        else:
            object = masalalar.page(1)
        return render(request, 'users/quizess.html', {'profile': profile, 'object_list': object, 'object': masalalar})
    
def onlines(request):
    users = MyUser.objects.all()
    return render(request, 'users/onlines.html', {'users': users})

def update_user_with_admin_view(request: HttpRequest, username):
    if request.user.is_staff:
        profile = get_object_or_404(MyUser, username=username)

        if request.method == "POST":
            first_name = request.POST.get('first_name')
            profile.first_name = first_name

            last_name = request.POST.get('last_name')
            profile.last_name = last_name

            email = request.POST.get('email')
            profile.email =email

            date_joined = request.POST.get('date_joined')
            profile.date_joined = date_joined
            
            username1 = request.POST.get('username')
            try:
                profile.username = username1
            except:
                messages.error('Kiritilgan foydalanuvchi nomi tizim qoidasiga to\'g\g\'ri kelmaydi.')
                return HttpResponseRedirect(f'/users/profile/{username}')
            if 'password' in request.POST:
                password = request.POST.get('password') if request.POST.get('password')!='' else None
                if password:
                    profile.set_password(password)
            is_staff=request.POST.get('is_staff')=='on'
            profile.is_staff =is_staff

            is_create_course = request.POST.get('is_create_course')=='on'
            profile.is_create_course = is_create_course

            is_create_test = request.POST.get('is_create_test')=='on'
            profile.is_create_test = is_create_test

            is_create_ass = request.POST.get('is_create_ass')=='on'
            profile.is_create_ass = is_create_ass

            is_create_masala = request.POST.get('is_create_masala')=='on'
            profile.is_create_masala = is_create_masala

            is_create_yechim = request.POST.get('is_create_yechim')=='on'
            profile.is_create_yechim = is_create_yechim

            is_create_bsb = request.POST.get('is_create_bsb')=='on'
            profile.is_create_bsb = is_create_bsb

            profile.save()
            messages.success(request, 'Foydalanuvchi muvaffaqiyatli tahrirlandi')
            return HttpResponseRedirect(f'/users/profile/{profile.username}/')

        return render(request, 'users/user_admin_admin.html', {'profile': profile}) if request.user!=profile else render(request, '404.html')
    return render(request, '404.html')