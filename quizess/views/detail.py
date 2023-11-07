import ast
from datetime import datetime
import json
from django.shortcuts import render, get_object_or_404
from quizess.models import ClosedTest, ClosedTestAnswer, DefaultQuizAnswer, DefoulMultitQuiz, DefoulMultitQuizAnswer, DefoultQuiz, DefoultQuizVariant, DragAndDropAnswer, DragAndDropVariants, Quiz, Result, StartedTime
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest
from django.contrib import messages
from datetime import datetime
from time import time as default_time

def all_view(request):
    tests = Quiz.objects.all().order_by('-id')
    masalalar = Paginator(tests, 10)
    if 'page' in request.GET:
        object = masalalar.page(request.GET['page'])
    else:
        object = masalalar.page(1)
    return render(request, 'tests/all.html', {'page_obj': object, 'object': masalalar,})

def delete_test(request, id):
    if request.user.is_authenticated:
        test = get_object_or_404(Quiz,id=id)
        if request.method=='POST':
            test.delete()
            messages.success(request, 'Test tizimdan o\'chirilib tashlandi!')
            return HttpResponseRedirect(f'/tests/')
        return render(request, 'tests/delete.html', {'test': test})
    else:
        return render(request, '403.html', status=403)

def deteil_view(request, id):
    if request.user.is_authenticated:
        test = get_object_or_404(Quiz,id=id)
        if test.is_public or request.user.is_staff or request.user == test.author:
            return render(request, 'tests/deteil.html', {'test': test})
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '/users/login/')

def start_test_view(request, id):
    if request.user.is_authenticated:
        test = get_object_or_404(Quiz,id=id)
        if test.is_public or request.user.is_staff or request.user == test.author:
            if test.quizes_count != 0:
                test.not_actioned_users.add(request.user)
                test.save()
                return HttpResponseRedirect(f'/tests/test/{id}/')
            else:
                return render(request, '403.html', status=403)
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '/users/login/')

def quizes_view(request: HttpRequest, id):
    if request.user.is_authenticated:
        test = get_object_or_404(Quiz,id=id)
        if test.is_public or request.user.is_staff or request.user == test.author:

            if test.quizes_count != 0 and request.user in test.not_actioned_users.all() and request.user not in test.users.all():
                started_time = StartedTime.objects.filter(user=request.user, quiz=test, time=test.time)
                if started_time.count()==0:
                    StartedTime.objects.create(user=request.user, quiz=test, time=test.time)

                quiz1 = list(test.default_quizes.all())
                quiz2 = list(test.default_closed_quizes.all())
                quiz3 = list(test.default_multi_quizes.all())
                quiz4 = list(test.drag_and_drop.all())
                all_objects = quiz1+quiz2+quiz3+quiz4
                sorted_objects = sorted(all_objects, key=lambda x: x.date_created)
                return render(request, 'tests/quizes.html', {'test': test, 'sorted_objects':sorted_objects, 'started_time': started_time})
            else:
                res = Result.objects.filter(user = request.user, test=test).first()
                messages.success(request, f'Siz ushbu testdan {res.score} ball olgansiz!')
                return HttpResponseRedirect(f'/tests/test/{test.id}/')
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '/users/login/')

def quizes_post_view(request, id):
    if request.user.is_authenticated:
        test = get_object_or_404(Quiz,id=int(id))
        if test.is_public or request.user.is_staff or request.user == test.author:

            if test.quizes_count != 0 and request.user in test.not_actioned_users.all() and request.user not in test.users.all():
                trues = []
                data1 = {}
                score = 0
                if request.method=='POST':
                    if len(request.POST.getlist('ml')[0])!=0:
                        ml = request.POST.getlist('ml')
                        ml = json.loads(ml[0])
                        for ml_key,ml_value in ml.items():
                            ml_key = int(ml_key)
                            df_quiz = test.default_multi_quizes.get(id=ml_key)
                            a=False
                            for idca in ml_value:
                                idca = int(idca)
                                variant = df_quiz.variants.get(id=idca)
                                if variant.is_true:
                                    a=True
                                else:
                                    a=False
                                    break
                            if a:
                                DefoulMultitQuizAnswer.objects.create(user=request.user, quiz=test, default_quiz=df_quiz, is_true=True)
                                trues.append(df_quiz)
                                score+=df_quiz.ball
                                data1[df_quiz.body] = True
                            else:
                                data1[df_quiz.body] = False
                                DefoulMultitQuizAnswer.objects.create(user=request.user, quiz=test, default_quiz=df_quiz, is_true=False)

                    if len(request.POST.getlist('cl')[0])!=0:
                        cl = request.POST.getlist('cl')
                        cl = json.loads(cl[0])
                        for i,v in cl.items():
                            i = int(i)
                            cl_test = ClosedTest.objects.get(id=i)
                            if cl_test.true_answer == v:
                                ClosedTestAnswer.objects.create(user=request.user, is_true=True, answer=cl_test.true_answer, closed_quiz=cl_test,quiz=test)
                                trues.append(cl_test)
                                score+=cl_test.ball
                                data1[cl_test.body] = True
                            else:
                                ClosedTestAnswer.objects.create(user=request.user, is_true=False, answer=cl_test.true_answer, closed_quiz=cl_test,quiz=test)
                                data1[cl_test.body] = False

                    if len(request.POST.getlist('dd_s')[0])!=0:
                        dd_s1 = request.POST.getlist('dd_s')
                        dd_s = json.loads(dd_s1[0])
                        for j, k in dd_s.items():
                            variant1 = DragAndDropVariants.objects.get(id=int(j))
                            a=False
                            for k1 in k:
                                variant2 = DragAndDropVariants.objects.get(id=int(k1))
                                if variant2.parent == variant1:
                                    a=True
                                else:
                                    a=False
                                    break
                            if a:
                                data1[variant1.quiz_dr.body] = True
                                DragAndDropAnswer.objects.create(actioned_user=request.user, is_true=True, quiz=test,answer='asd', test=variant1.quiz_dr)
                                trues.append(variant1.quiz_dr)
                                score+=variant1.quiz_dr.ball
                            else:
                                data1[variant1.quiz_dr.body] = False
                                DragAndDropAnswer.objects.create(actioned_user=request.user, is_true=False, quiz=test,answer='asd', test=variant1.quiz_dr)

                    if len(request.POST.getlist('dq')[0])!=0:
                        dq = request.POST.getlist('dq')
                        dq = json.loads(dq[0])
                        for u, y in dq.items():
                            u = int(u)
                            y = int(y)
                            quizca = DefoultQuiz.objects.get(id=u)
                            variantca = DefoultQuizVariant.objects.get(id=y)
                            if variantca.is_true:
                                data1[quizca.body] = True
                                DefaultQuizAnswer.objects.create(user=request.user, quiz=test, is_true=True, default_quiz=quizca)
                                trues.append(quizca)
                                score+=quizca.ball
                            else:
                                data1[quizca.body] = False
                                DefaultQuizAnswer.objects.create(user=request.user, quiz=test, is_true=False, default_quiz=quizca)

                    time = request.POST.get('time')
                    res = Result.objects.create(user=request.user, score=score, test=test, data=data1, time=datetime.strptime(time, "%H:%M:%S"))
                    test.users.add(request.user)
                    request.user.ball+=score
                    request.user.save()
                    messages.success(request, f'Siz ushbu testdan {res.score} ball oldingiz!')
                    return JsonResponse({'status': 'ok1', 'data':res.data})
                else:
                    return JsonResponse({'status':'This Method not allowed'})
            else:
                res = Result.objects.filter(user = request.user, test=test).first()
                messages.success(request, f'Siz ushbu testdan {res.score} ball olgansiz!')
                return HttpResponseRedirect(f'/tests/test/{test.id}/')
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '/users/login/')


def get_started_time_api(request: HttpRequest, id):
    if request.user.is_authenticated:
        test = get_object_or_404(Quiz,id=id)
        if test.is_public or request.user.is_staff or request.user == test.author:

            if test.quizes_count != 0 and request.user in test.not_actioned_users.all() and request.user not in test.users.all():
                return JsonResponse({'time': StartedTime.objects.filter(user=request.user,quiz=test).first().total_seconds(), 'start': StartedTime.objects.filter(user=request.user,quiz=test).first().get_t_1()})
            else:
                res = Result.objects.filter(user = request.user, test=test).first()
                messages.success(request, f'Siz ushbu testdan {res.score} olgansiz!')
                return HttpResponseRedirect(f'/tests/test/{test.id}/')
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '/users/login/')

def public_api(request: HttpRequest, id):
    if request.user.is_authenticated:
        test = get_object_or_404(Quiz,id=id)
        if request.user.is_staff or request.user.is_teacher:
            test.is_public = True
            test.save()
            messages.success(request, f'Test Ommaviy qilindi')
            return HttpResponseRedirect(f'/tests/test/{test.id}/')
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '/users/login/')

def results_view(request, id):
    test = get_object_or_404(Quiz, id=id)
    results = test.results.all().order_by('-score', '-time')
    masalalar = Paginator(results, 40)
    page = 1
    if 'page' in request.GET:
        page = int(request.GET.get('page'))
    object = masalalar.page(page)
    return render(request, 'tests/results.html', {'test': test, 'object':results, 'page_obj':object, 'page': page})

def result_view(request, id):
    test = get_object_or_404(Quiz, id=id)
    if request.user.is_authenticated:
        result = Result.objects.filter(user=request.user, test=test)
        if result.count()!=0:
            result = result.last()
            return render(request, 'tests/result.html', {'test': test, 'result': result})
        else:
            return render(request, '404.html', status=404)
    else:
        return render(request, '404.html', status=404)

def result1_view(request, id, id1):
    test = get_object_or_404(Quiz, id=id)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == test.author:
            result = get_object_or_404(Result, id=id1)
            return render(request, 'tests/result1.html', {'test': test, 'result': result})
        else:
            return render(request, '404.html', status=404)
    else:
        return render(request, '404.html', status=404)