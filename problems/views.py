import json
from re import T
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from .models import Problem, TaskComment
from .forms import TaskForm, TaskEditForm, AttemptForm
from django.contrib import messages
from attempts.models import Attempt
from .complier import Complier
from assignments.models import Assignment, StudentAnswer, StudentAnswerComments


def task_detail(request, task_id):
    unread_assign = None
    unread_answerca2 = []
    if request.user.is_authenticated:
        unread_assign = Assignment.objects.filter(
            is_readed=False, student=request.user)

        unread_answerca = StudentAnswer.objects.filter(is_readed=False)
        unread_answerca2 = []
        for unread_answerca1 in unread_answerca:

            if unread_answerca1.assignment.author == request.user:
                a = unread_answerca1
                unread_answerca2.append(a)

    task = get_object_or_404(Problem, id=task_id)
    task_attempts = None
    attemptca = None
    formca = None
    if request.user.is_authenticated:
        attemptca = Attempt.objects.filter(
            problem=task, author=request.user).last()
        formca = AttemptForm(request.POST or None, instance=attemptca)
        task_attempts = Attempt.objects.filter(
            author=request.user, problem=task).order_by('-id')
    task_attempts1 = Attempt.objects.filter(problem=task).order_by('-id')
    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'comment_body' in request.POST:
                TaskComment(user=request.user, problem=task,
                            body=request.POST['comment_body']).save()
                messages.success(request, 'Komentariya joylashtirildi!')
                return HttpResponseRedirect(f'/informatics/problems/problem/{task.id}/')
            if 'code' in request.POST:
                runner = Complier(
                    body=request.POST['code'], time_limit=task.time_limit, memory_limit=task.memory_limit, tests=task.tests)
                data = runner.run()
                Attempt(problem=task, author=request.user, code=request.POST['code'], holat=data['status'], time=float(
                    '%.2f' % (data['time']*1000)), memory=runner.get_run_memory()*1024).save()
                if data['status'] == 'Accepted':
                    wrong_answers = Attempt.objects.filter(
                        author=request.user,
                        problem=task).exclude(holat='Accepted')
                    accepteds = task.problem_attempt.filter(holat='Accepted')
                    if wrong_answers.count() > accepteds.count():
                        all = wrong_answers.count() + accepteds.count()
                        foiz3 = (wrong_answers.count() / all)*100
                        foiz2 = (accepteds.count() / all)*100
                        foiz1 = foiz2-foiz3
                    else:
                        all = wrong_answers.count() + accepteds.count()
                        foiz3 = (wrong_answers.count() / all) * 100
                        foiz2 = (accepteds.count() / all) * 100
                        foiz1 = foiz2 - foiz3
                    task.foiz = foiz1
                    task.accepteds.add(request.user)
                    messages.success(request, 'Accepted')
                    task.save()
                else:
                    if request.user in task.accepteds.all():
                        pass
                    else:
                        task.wrong_answers.add(request.user)
                        wrong_answers = Attempt.objects.filter(
                            author=request.user,
                            problem=task).exclude(holat='Accepted')
                        accepteds = task.problem_attempt.filter(
                            holat='Accepted')
                        if wrong_answers.count() > accepteds.count():
                            all = wrong_answers.count() + accepteds.count()
                            foiz3 = (wrong_answers.count() / all) * 100
                            foiz2 = (accepteds.count() / all) * 100
                            foiz1 = foiz2 - foiz3
                        else:
                            all = wrong_answers.count() + accepteds.count()
                            foiz3 = (wrong_answers.count() / all) * 100
                            foiz2 = (accepteds.count() / all) * 100
                            foiz1 = foiz2 - foiz3
                        task.foiz = foiz1
                        messages.error(request, data['status'])
                        task.save()
                return HttpResponseRedirect(f'/informatics/problems/problem/{task.id}/')
        else:
            return render(request, '404.html')
    return render(request, 'problems/problem.html', {'task': task, 'task_attempts': task_attempts, 'task_attempts1': task_attempts1, 'formca': formca, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})


def add_tasks(request):
    unread_assign = None
    unread_answerca2 = []
    if request.user.is_authenticated:
        unread_assign = Assignment.objects.filter(
            is_readed=False, student=request.user)

        unread_answerca = StudentAnswer.objects.filter(is_readed=False)
        unread_answerca2 = []
        for unread_answerca1 in unread_answerca:

            if unread_answerca1.assignment.author == request.user:
                a = unread_answerca1
                unread_answerca2.append(a)
    if request.user.is_authenticated:
        if request.user.is_teacher or request.user.is_staff:
            if request.method == 'POST':
                title = request.POST.get('title')
                body = request.POST.get('body')
                info_in = request.POST.get('info_in')
                info_out = request.POST.get('info_out')
                difficulty = request.POST.get('difficulty')
                memory = request.POST.get('memory')
                time = request.POST.get('time')
                solve = request.POST.get('solve')
                tests = request.POST.get('tests')
                simple = request.POST.get('simple_tests')
                try:
                    tests = json.loads(tests)
                except:
                    messages.error('Siz kiritgan testlar yaroqli emas!')
                    return render(request, 'problems/add_task.html', {'title':title,'body':body,'info_in': info_in,'info_out':info_out, 'diff': difficulty,'memory': memory,'time': time, 'solve': solve,'tests':tests,'simple':simple})
                try:
                    simple = json.loads(simple)
                except:
                    messages.error('Siz kiritgan misollar yaroqli emas!')
                    return render(request, 'problems/add_task.html', {'title':title,'body':body,'info_in': info_in,'info_out':info_out, 'diff': difficulty,'memory': memory,'time': time, 'solve': solve,'tests':tests,'simple':simple})
                problem = Problem.objects.create(author=request.user, title=title, time_limit=time, memory_limit=memory, difficulty=difficulty,
                                                 about=body, info_in=info_in, info_out=info_out, simple_tests=simple, tests=tests, yechim=solve)
                messages.success(request, 'Masalangiz muvoffiqiyatli tizimga qo\'shildi')
                return HttpResponseRedirect(f'/informatics/problems/problem/{problem.id}/')
            return render(request, 'problems/add_task.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def edit_task(request, task_id):
    unread_assign = None
    unread_answerca2 = []
    if request.user.is_authenticated:
        unread_assign = Assignment.objects.filter(
            is_readed=False, student=request.user)

        unread_answerca = StudentAnswer.objects.filter(is_readed=False)
        unread_answerca2 = []
        for unread_answerca1 in unread_answerca:

            if unread_answerca1.assignment.author == request.user:
                a = unread_answerca1
                unread_answerca2.append(a)
    problem = get_object_or_404(Problem, id=task_id)
    simple = json.dumps(problem.simple_tests)
    tests = json.dumps(problem.tests)
    if request.user.is_authenticated:
        if request.user.is_teacher or request.user.is_staff:
            if request.method == 'POST':
                title = request.POST.get('title')
                problem.title = title
                body = request.POST.get('body')
                problem.about = body
                info_in = request.POST.get('info_in')
                problem.info_in = info_in
                info_out = request.POST.get('info_out')
                problem.info_out = info_out
                difficulty = request.POST.get('difficulty')
                problem.difficulty = difficulty
                memory = request.POST.get('memory')
                problem.memory_limit = memory
                time = request.POST.get('time')
                problem.time_limit = time
                solve = request.POST.get('solve')
                problem.yechim = solve
                tests = request.POST.get('tests')
                simple = request.POST.get('simple_tests')
                try:
                    tests = json.loads(tests)
                except:
                    messages.error(request, 'Siz kiritgan testlar yaroqli emas!')
                    return render(request, 'problems/add_task.html', {'title':title,'body':body,'info_in': info_in,'info_out':info_out, 'diff': difficulty,'memory': memory,'time': time, 'solve': solve,'tests':tests,'simple':simple})
                try:
                    simple = json.loads(simple)
                except:
                    messages.error(request, 'Siz kiritgan misollar yaroqli emas!')
                    return render(request, 'problems/add_task.html', {'title':title,'body':body,'info_in': info_in,'info_out':info_out, 'diff': difficulty,'memory': memory,'time': time, 'solve': solve,'tests':tests,'simple':simple})
                problem.tests = tests
                problem.simple_tests = simple
                problem.save()
                messages.success(request, 'Masalangiz muvoffiqiyatli tahrirlandi.')
                return HttpResponseRedirect(f'/informatics/problems/problem/{problem.id}/')
            return render(request, 'problems/edit_task.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2), 'problem': problem, 'tests': tests, 'simple': simple})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def tasks(request):
    unread_assign = None
    unread_answerca2 = []
    if request.user.is_authenticated:
        unread_assign = Assignment.objects.filter(
            is_readed=False, student=request.user)

        unread_answerca = StudentAnswer.objects.filter(is_readed=False)
        unread_answerca2 = []
        for unread_answerca1 in unread_answerca:

            if unread_answerca1.assignment.author == request.user:
                a = unread_answerca1
                unread_answerca2.append(a)

    tasks = Problem.objects.all()
    attempts = []
    if request.user.is_authenticated:
        attempts = Attempt.objects.filter(author=request.user)
    return render(request, 'problems/tasks.html', {'tasks': tasks, 'attempts': attempts, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
