from django.shortcuts import render
import random, json as default_json, ast
import re
import string
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.core.paginator import Paginator
from olimpiads.models import Olimpiada, Problem
from users.models import MyUser
from django.db.models import Q
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.contrib import messages


def all_view(request: HttpRequest):
    olimpiadalar = Olimpiada.objects.all().order_by('-id')

    search = ''
    if 'search' in request.GET:
        search = str(request.GET.get('search'))
        olimpiadalar = olimpiadalar.filter(Q(title__icontains=search) | Q(author__username__icontains=search) |Q(author__first_name__icontains=search) | Q(author__last_name__icontains=search) | Q(url__icontains=search))

    masalalar = Paginator(olimpiadalar, 15)
    if 'page' in request.GET:
        object = masalalar.page(request.GET['page'])
    else:
        object = masalalar.page(1)
    return render(request, 'o/all.html', {'page_obj': object, 'object': masalalar, 'search': search})

def get_sol_view(request: HttpRequest, id):
    sol = get_object_or_404(Olimpiada, id=id)
    return render(request, 'o/detail.html', {'sol': sol})

def get_problem_view(request, id, id1):
    sol = get_object_or_404(Olimpiada, id=id)
    pr = get_object_or_404(Problem, id=id1, olimpiada=sol)
    return render(request, 'o/pr.html', {'sol':sol, 'pr':pr})

def add_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_teacher:
            if request.method == 'POST':
                title = request.POST.get('title')
                url = request.POST.get('url')
                ol = Olimpiada.objects.create(title=title,url=url, author=request.user)
                messages.success(request, 'Olimpiada Muvaffaqiyatli tizimga qo\'shildi!')
                return HttpResponseRedirect(f'/olympiad-solutions/solution/{ol.id}/')
        return render(request, 'o/add.html', )
    return render(request, '403.html', status=403)

def edit_view(request, id):
    sol = get_object_or_404(Olimpiada, id=id)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == sol.author:
            if request.method == 'POST':
                title = request.POST.get('title')
                sol.title = title
                url = request.POST.get('url')
                sol.url = url
                sol.save()
                messages.success(request, 'Olimpiada Muvaffaqiyatli tahrirlandi!')
                return HttpResponseRedirect(f'/olympiad-solutions/solution/{sol.id}/')
        return render(request, 'o/edit.html', {'sol': sol})
    return render(request, '403.html', status=403)

def add_solution1_view(request, id):
    sol = get_object_or_404(Olimpiada, id=id)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == sol.author:
            if request.method == 'POST':
                title = request.POST.get('title')
                url = request.POST.get('url')
                body = request.POST.get('body')
                pr = Problem.objects.create(title=title,url=url,yechim=body,olimpiada=sol, author=request.user)
                messages.success(request, 'Masala Muvaffaqiyatli qo\'shildi!')
                return HttpResponseRedirect(f'/olympiad-solutions/solution/{sol.id}/problem/{pr.id}/')
        return render(request, 'o/add1.html', {'sol': sol})
    return render(request, '403.html', status=403)

def edit2_view(request, id, id1):
    sol = get_object_or_404(Olimpiada, id=id)
    pr = get_object_or_404(Problem, id=id1, olimpiada=sol)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == sol.author:
            if request.method == 'POST':
                title = request.POST.get('title')
                pr.title = title
                url = request.POST.get('url')
                pr.url = url
                body = request.POST.get('body')
                pr.yechim = body
                pr.save()
                messages.success(request, 'Masala Muvaffaqiyatli tahrirlandi!')
                return HttpResponseRedirect(f'/olympiad-solutions/solution/{sol.id}/problem/{pr.id}/')
        return render(request, 'o/edit2.html', {'sol': sol, 'pr': pr})
    return render(request, '403.html', status=403)