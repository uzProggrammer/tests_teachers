import random, json as default_json, ast
import re
import string
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from .models import Masala, MasalaTeg, Teg, Testlar, Urinish, Likelar
from users.models import MyUser
from django.db.models import Q
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from .thread import UrinishYaratuvchiThread
from django.contrib import messages


def get_all_view(request):
    masalalar = Masala.objects.filter(is_archived=True)
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
    return render(request, 'masalalar/all.html', {'page_obj': object, 'object': masalalar, 'search': seach, 'type': type1})

def get_all_view1(request):
    masalalar = Masala.objects.filter(is_archived=False)
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
    return render(request, 'masalalar/all.html', {'page_obj': object, 'object': masalalar, 'search': seach, 'type': type1})


def masala_view(request: HttpRequest, slug):
    masala = get_object_or_404(Masala, slug=slug, is_archived=True)
    attempts = []
    user_like = False
    user_dislike = False
    if request.user.is_authenticated:
        attempts = Urinish.objects.filter(masala=masala, user=request.user).order_by('-id')
        dislikes = Likelar.objects.filter(type='dislike', user=request.user, masala=masala)
        likes = Likelar.objects.filter(type='like', user=request.user, masala=masala)
        if dislikes.count() != 0:
            user_dislike = True
            user_like = False
        elif likes.count() != 0:
            user_dislike = False
            user_like = True
        if request.method == 'POST':
            lang = request.POST.get('lang')
            code = ''
            if 'code' in request.POST:
                emptys = Masala.objects.filter(empty=False)
                if emptys.count() != 0:
                    code = request.POST.get('code')
                    urinish = Urinish.objects.create(user=request.user, masala=masala, tests={
                     }, memory=0, time=0, olcham=len(code), til=lang, turi='Navbatda', body=code)
                    UrinishYaratuvchiThread(request.user.username, masala, lang, urinish).start()
                else:
                    code = request.POST.get('code')
                    urinish = Urinish.objects.create(user=request.user, masala=masala, tests={
                    }, memory=0, time=0, olcham=len(code), til=lang, turi='Tekshirilmoqda', body=code)
                    
                    UrinishYaratuvchiThread(request.user.username, masala, lang, urinish).start()
                messages.success(request, urinish.turi)
                return HttpResponseRedirect(f'/informatics/problems/problem/{masala.slug}/')
    return render(request, 'masalalar/masala.html', {'masala': masala, 'attempts':attempts, 'user_like':user_like, 'user_dislike': user_dislike})

def like_toggle_view(request, slug):
    masala = get_object_or_404(Masala, slug=slug)
    if request.user.is_authenticated:
        if 'type' in request.GET:
            type=request.GET.get('type')
            like = Likelar.objects.get_or_create(user=request.user, masala=masala)
            if type == 'like' or type == 'dislike':
                like[0].type = type
                like[0].save()
                dislikes = Likelar.objects.filter(type='dislike').count()
                likes = Likelar.objects.filter(type='like').count()
                return JsonResponse({'status': 'ok', 'count1': dislikes, 'likes': likes})
            else:
                return JsonResponse({'status': 'Failed'})
        else:
            return JsonResponse({'status': 'Failed'})
    else:
        return JsonResponse({'status': 'Failed'})

def get_masala_urinishlar_view(request: HttpRequest, slug):
    masala = get_object_or_404(Masala, slug=slug)
    urinishlar = masala.urinishlar.all().order_by('-id')
    masalalar = Paginator(urinishlar, 40)
    if 'page' in request.GET:
        object = masalalar.page(request.GET['page'])
    else:
        object = masalalar.page(1)
    return render(request, 'attempts/all_form_problem.html', {'masala': masala, 'object':urinishlar, 'page_obj':object})


def rating(request, slug, type1):
    masala = get_object_or_404(Masala, slug=slug)
    urinishlar = Urinish.objects.filter(masala=masala, turi='Qabul Qilindi')

    if type1!='len' and type1!='memory' and type1!='time':
        return HttpResponseNotFound()

    urinishlar = urinishlar.order_by('olcham' if type1=='len' else 'memory' if type1 == 'memory' else 'time')
    masalalar = Paginator(urinishlar, 40)
    if 'page' in request.GET:
        object = masalalar.page(request.GET['page'])
    else:
        object = masalalar.page(1)
    return render(request, 'attempts/rating.html', {'masala': masala, 'object':urinishlar, 'page_obj':object})

def masala_qoshish(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_teacher:
            if request.method == 'POST':
                title = request.POST.get('title')
                diff = request.POST.get('diff')
                memory = request.POST.get('memory')
                time = request.POST.get('time')

                body = '...'
                if 'body' in request.POST:
                    body = request.POST.get('body')
                
                _in = None
                if 'in' in request.POST:
                    _in = request.POST.get('in')
                
                out = None
                if 'out' in request.POST:
                    out = request.POST.get('out')
                
                checker = None
                if 'checker' in request.POST:
                    checker = request.POST.get('checker')

                type = request.POST.get('type')

                yechim = None
                if 'yechim' in  request.POST:
                    yechim = request.POST.get('yechim')

                testcases = request.POST.get('testcases')

                letters = string.ascii_letters
                digits = string.digits
                all_ch = letters+digits
                pwd_length = 40
                pwd = ''.join(random.sample(all_ch, pwd_length))

                if 'teg' in request.POST:
                    tegs = request.POST.getlist('teg')
                    for teg in tegs:
                        teg1 = Teg.objects.create(name=teg)
                        MasalaTeg.objects.create(problem=masala,tag=teg1)

                masala = Masala.objects.create(title=title, difficulty=diff, memory_limit=memory, time_limit=time, body=body,
                    info_in=_in, out=out, checker=checker, type=type, yechim = yechim, korinadigan_testlar = testcases, slug=pwd, author=request.user
                )
                messages.success(request, 'Masala muvvofiqiyatli yaratildi')
                return HttpResponseRedirect(f'/informatics/problems/unproblem/{masala.slug}/')
            return render(request, 'masalalar/create.html', )
        else:
            return render(request, '403.html', {'messege': 'Siz ushbu sahifaga tashrif buyura olmaysiz!'}, status=403)
    else:
        return render(request, '403.html', {'messege': 'Siz ushbu sahifaga tashrif buyura olmaysiz!'}, status=403)

def masalaemas_view(request: HttpRequest, slug):
    masala = get_object_or_404(Masala, slug=slug, is_archived=False)
    attempts = []
    user_like = False
    user_dislike = False
    if request.user.is_authenticated:
        attempts = Urinish.objects.filter(masala=masala, user=request.user).order_by('-id')
        dislikes = Likelar.objects.filter(type='dislike', user=request.user, masala=masala)
        likes = Likelar.objects.filter(type='like', user=request.user, masala=masala)
        if dislikes.count() != 0:
            user_dislike = True
            user_like = False
        elif likes.count() != 0:
            user_dislike = False
            user_like = True
        if request.method == 'POST':
            code = ''
            if 'code' in request.POST:
                lang = request.POST.get('lang')
                emptys = Masala.objects.filter(empty=False)
                if emptys.count() != 0:
                    code = request.POST.get('code')
                    urinish = Urinish.objects.create(user=request.user, masala=masala, tests={
                    }, memory=0, time=0, olcham=len(code), til=lang, turi='Navbatda', body=code)
                    UrinishYaratuvchiThread(request.user.username, masala, lang, urinish).start()
                else:
                    code = request.POST.get('code')
                    urinish = Urinish.objects.create(user=request.user, masala=masala, tests={
                    }, memory=0, time=0, olcham=len(code), til=lang, turi='Tekshirilmoqda', body=code)
                    
                    UrinishYaratuvchiThread(request.user.username, masala, lang, urinish).start()
                messages.success(request, urinish.turi)
                return HttpResponseRedirect(f'/informatics/problems/unproblem/{masala.slug}/')
    return render(request, 'masalalar/masala.html', {'is_unproblem': True, 'masala': masala, 'attempts':attempts, 'user_like':user_like, 'user_dislike': user_dislike})

def testcases(request, slug):
    masala = get_object_or_404(Masala, slug=slug)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == masala.author:
            testcases = masala.testlar.all()
            masalalar = Paginator(testcases, 50)
            json = False
            if 'from-json' in request.GET:
                json = True
            
            json1 = ''
            if request.method == 'POST':
                if 'json' in request.POST:
                    json1 = request.POST.get('json')
                    try:
                        json1 = ast.literal_eval(json1)
                        for key, value in json1.items():
                            Testlar.objects.create(t_in=key, out=value, masala=masala)

                        messages.success(request, 'Muffofiqityatli testlat qo\'shildi')
                        return HttpResponseRedirect(f'/informatics/problems/unproblem/{masala.slug}/testcases')
                    except:
                        messages.error(request, "Siz kiritgan Json ma'lumoti to'g'ri emas. Iltimos qaytadan urinib ko'ring!")

            if 'page' in request.GET:
                object = masalalar.page(request.GET['page'])
            else:
                object = masalalar.page(1)
            return render(request, 'masalalar/testcases.html', {'masala': masala,'page_obj': object, 'object': masalalar, 'json':json, 'json1': json1})
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '403.html', status=403)

def testcases_post_view(request, slug):
    masala = get_object_or_404(Masala, slug=slug)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == masala.author:
            if request.method == 'POST':
                key = request.POST.get('key')
                value = request.POST.get('value')
                Testlar.objects.create(t_in=key,out=value,masala=masala)
                return JsonResponse({'status': 'ok'})
            else:
                return render(request, '403.html', status=403)
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '403.html', status=403)
    
def to_archive(request: HttpRequest, slug):
    masala = get_object_or_404(Masala, slug=slug)
    if request.user.is_authenticated:
        if request.user.is_staff:
            masala.is_archived = True
            masala.save()
            messages.success(request, 'Masala muvvofiqiyatli arxivlandi')
            return HttpResponseRedirect(f'/informatics/problems/problem/{masala.slug}/')
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '403.html', status=403)

def add_yechim_view(request, slug):
    masala = get_object_or_404(Masala, slug=slug)
    if request.user.is_authenticated:
        if request.user.is_staff and masala.yechim:
            masala.have_yechim = True
            masala.save()
            messages.success(request, 'Masala yechimi muvvofiqiyatli qo\'shildi')
            if masala.is_archived:
                return HttpResponseRedirect(f'/informatics/problems/problem/{masala.slug}/')
            else:
                return HttpResponseRedirect(f'/informatics/unproblems/problem/{masala.slug}/')
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '403.html', status=403)

def yechim_view(request, slug):
    masala = get_object_or_404(Masala, slug=slug)
    if request.user.is_authenticated:
        if request.user.is_staff and masala.yechim:
            return render(request, f'masalalar/yechim.html', {"masala":masala})
        else:
            return render(request, '404.html', status=404)
    else:
        return render(request, '403.html', status=403)


def edit_testcase_view(request, slug):
    masala = get_object_or_404(Masala, slug=slug)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == masala.author:
            if request.method == 'POST':
                id = request.POST.get('id')
                key = request.POST.get('key')
                value = request.POST.get('value')
                test = Testlar.objects.get(id=id)
                test.t_in = key
                test.out = value
                test.save()
                messages.success(request, 'Testcase muvvofiqiyatli tahrirlandi')
                return JsonResponse({'status': 'ok'})
            else:
                return HttpResponseNotFound()
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '403.html', status=403)
        
def urinishlar_view(request):
    masalalar = Paginator(Urinish.objects.all().order_by('-id'), 20)
    if 'page' in request.GET:
        object = masalalar.page(request.GET['page'])
    else:
        object = masalalar.page(1)
    return render(request, 'attempts/all.html', {'object_list': object, 'object': masalalar})

def urinish_view(request, id):
    urinish = get_object_or_404(Urinish, id=id)
    if request.user.is_authenticated:
        if request.user == urinish.user or request.user.is_staff:
            return render(request, 'attempts/attempt.html', {'urinish': urinish})
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '403.html', status=403)

def masala_tahrirla_view(request, slug):
    masala = get_object_or_404(Masala, slug=slug)
    if request.user.is_authenticated:
        if request.user == masala.author or request.user.is_staff:
            if request.method == 'POST':
                title = request.POST.get('title')
                masala.title = title

                diff = request.POST.get('diff')
                masala.difficulty = diff

                memory = request.POST.get('memory')
                masala.memory_limit = memory

                time = request.POST.get('time')
                masala.time_limit = time

                body = '...'
                if 'body' in request.POST:
                    body = request.POST.get('body')
                masala.body = body

                _in = None
                if 'in' in request.POST:
                    _in = request.POST.get('in')
                masala.info_in = _in


                out = None
                if 'out' in request.POST:
                    out = request.POST.get('out')
                masala.out = out

                checker = None
                if 'checker' in request.POST:
                    checker = request.POST.get('checker')
                masala.checker = checker

                type = request.POST.get('type')
                masala.type = type

                yechim = None
                if 'yechim' in  request.POST:
                    yechim = request.POST.get('yechim')
                masala.yechim = yechim

                testcases = request.POST.get('testcases')
                masala.korinadigan_testlar = testcases

                if 'teg' in request.POST:
                    tegs = request.POST.getlist('teg')
                    for teg in tegs:
                        teg1 = Teg.objects.create(name=teg)
                        MasalaTeg.objects.create(problem=masala,tag=teg1)
                masala.save()
                messages.success(request, 'Masala muvvofiiqiyatli tahrirlandi')
                if masala.is_archived:
                    return HttpResponseRedirect(f'/informatics/problems/problem/{masala.slug}/')
                else:
                    return HttpResponseRedirect(f'/informatics/problems/unproblem/{masala.slug}/')
            return render(request, 'masalalar/edit.html', {'masala': masala})
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '403.html', status=403)
