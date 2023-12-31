from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from bsb.models import BSB
from users.models import MyUser
from .models import Baho
from sinflar.models import Sinf
from django.utils import timezone
import collections


def baho(request, username):
    if request.user.is_authenticated:
        profile = get_object_or_404(MyUser, username=username)
        baholar = profile.baholar.all()
        object = Paginator(baholar, 40)

        if 'page' in request.GET:
            object = object.page(request.GET['page'])
        else:
            object = object.page(1)
        return render(request, 'baho/baho.html',{'profile': profile, 'object': object,})
    else:
        return render(request, '404.html')

def assignment_baho(request, username):
    if request.user.is_authenticated and not request.user.is_staff and not request.user.is_teacher:
        profile = get_object_or_404(MyUser, username=username)
        answers = profile.assignment_answers.all()
        object = Paginator(answers, 40)

        if 'page' in request.GET:
            object = object.page(request.GET['page'])
        else:
            object = object.page(1)
        return render(request, 'baho/ass_price.html', {'profile': profile, 'answers':answers, 'object':object})
    else:
        return render(request, '404.html', status=404)

def bsb_ball(request, username):
    if request.user.is_authenticated and not request.user.is_staff and not request.user.is_teacher:
        profile = get_object_or_404(MyUser, username=username)
        sinf = get_object_or_404(Sinf, nom=profile.sinf)
        bsb = BSB.objects.filter(sinf=sinf)
        problem_bal = {}
        test_ball = {}
        ass_ball = {}
        for control in bsb:
            if control.type=='Topshiriq':
                ball = 0
                for i in control.assignments.all():
                    try:
                        ball+=i.answers.filter(user=profile).first().answer_balls.first().ball
                    except:
                        pass
                ass_ball[control.id]=ball
            if control.type=='Test':
                try:
                    test_ball[control.id]=control.balls.get(user=profile).scope
                except:
                    pass
            if control.type == 'Masala':
                for problem in control.problems.all():
                    for answer in problem.answers.all():
                        if answer.balls.exists and answer.type == 'Accepted':

                            problem_bal[control]=answer.balls.first()
                            break
        object = Paginator(bsb, 40)

        if 'page' in request.GET:
            object = object.page(request.GET['page'])
        else:
            object = object.page(1)
        return render(request, 'baho/control_price.html', {'profile': profile, 'object':object, 'problem_bal':problem_bal, 'test_ball':test_ball,'ass_ball':ass_ball})
    else:
        return render(request, '404.html', status=404)

# def class_baho(request, slug):
#     if request.user.is_authenticated:
#         sinf = Sinf.objects.get(url=slug)
#         datesca = [
#             'Dushanba',
#             'Seshanba',
#             'Chorshnba',
#             'Payshanba',
#             'Juma',
#             'Shanba',
#             'Yakshanba'
#         ]
#         now = timezone.now()
#         date_week = now.weekday()
#         dates = []
#         for user in sinf.students.all():
#             for baho in user.baholar.all():
#                 if baho.bsb:
#                     date = baho.bsb.date_statrted
#                 else:
#                     date = baho.assignment.date_created
#                 dates.append(date)
#         collections.OrderedDict(sorted(dates.items()))
#         dates.sort()
#         return render(request, 'baho/jurnal.html', {'sinf':sinf, 'datesca':datesca, 'date_week':date_week, 'dates':dates})
#     else:
#         return render(request, '404.html')