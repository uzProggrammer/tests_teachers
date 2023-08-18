from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import TaskCkEditForm, RichTask
from assignments.models import Assignment, StudentAnswer

def all_tests(request):
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

    tests = Task.objects.all()
    return render(request, 'tests/all_tests.html', {'tests': tests, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def test_detail(request, id):
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

    test = get_object_or_404(Task, id=id)
    if test.author == request.user and test.is_active==False:
        in_test = False
        if request.method == 'POST':
            if request.user in test.users.all():
                in_test = False
                test.users.remove(request.user)
            else:
                in_test = True
                test.users.add(request.user)
        qatnashgan = False
        if request.user in test.actioned_users.all():
            qatnashgan = True
        return render(request, 'tests/test_detail.html', {'test': test, 'qatnashgan': qatnashgan, 'in_test':in_test, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    elif test.is_active:
        in_test = False
        if request.method == 'POST':
            if request.user in test.users.all():
                in_test = False
                test.users.remove(request.user)
            elif request.user.is_authenticated:
                in_test = True
                test.users.add(request.user)
            else:
                in_test = False
        qatnashgan = False
        if request.user in test.actioned_users.all():
            qatnashgan = True
        return render(request, 'tests/test_detail.html', {'test': test, 'qatnashgan': qatnashgan, 'in_test': in_test, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    else:
        return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def questions(request, id):
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

    test = get_object_or_404(Task, id=id)
    if request.user in test.users.all() and request.user not in test.actioned_users.all():
        questions = test.answer.all()

        return render(request, 'tests/questions.html', {'questions':questions, 'test': test, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    else:
        return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def questions_post(request, id):
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

    data = {}
    data1=[]
    test = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                quiz = TaskQuestion.objects.get(id=key)
                answer = QuestionAnswers.objects.get(id=value)
                if answer.is_true:
                    data[quiz.id] = True
                    data1.append(1)
                else:
                    data[quiz.id] = False
        scopes = test.ball * len(data1)
        Result.objects.create(test=test, user=request.user, scope=scopes).save()
        user = MyUser.objects.get(username=request.user.username)
        user.ball += test.ball * len(data1)
        user.save()
        test.actioned_users.add(request.user)
        return render(request, 'tests/questions_post.html', {'data':data,'scope': scopes, 'test': test, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    else:
        ball = Result.objects.get(user=request.user,test=test)
        return render(request, 'tests/test_ended.html', {'unread_assign': unread_assign, 'test': test, 'unread_answerca': len(unread_answerca2), 'ball':ball})

def add_test(request):
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

    if request.user.is_staff or request.user.is_teacher:
        if request.method == 'POST':
            form = TaskCkEditForm(request.POST)
            inctance = form.save(commit=False)
            inctance.author = request.user
            inctance.save()
            last_ = Task.objects.order_by('-pk')[0]
            return HttpResponseRedirect(f'/tests/test/{last_.id}/')
        form = TaskCkEditForm()
        return render(request, 'tests/add_test.html', {'form':form, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    else:
        return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def test_add_1(request, id):
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

    test = Task.objects.get(id=id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_teacher:
                quiz = request.POST
                TaskQuestion(task=test, body=request.POST['quiz-title']).save()
                new_answer = TaskQuestion.objects.last()
                is_true = int(request.POST['is_true'])
                for answer_key, answer_value in quiz.items():
                    if answer_key == 'csrfmiddlewaretoken' or answer_key == 'quiz-title' or answer_key == 'is_true':
                        pass
                    else:
                        if int(answer_key.split('-')[-1])==is_true:
                            QuestionAnswers(question=new_answer, body=answer_value, is_true=True).save()
                        else:
                            QuestionAnswers(question=new_answer, body=answer_value).save()
                return HttpResponseRedirect(f'/tests/test/{test.id}/')
            else:
                return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
        else:
            return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    else:
        return render(request, 'tests/add_test_1.html', {"test": test, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def actived_test(request, id):
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

    if request.method == 'GET':
        if request.user.is_staff or request.user.is_teacher:
            try:
                test = Task.objects.get(id=id)
                test.is_active = True
                test.save()
                return HttpResponseRedirect(f'/tests/test/{test.id}/')
            except Task.DoesNotExist:
                return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
        else:
            return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    else:
        return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def edit_test(request, id):
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

    try:
        task = Task.objects.get(id=id)
        form = TaskCkEditForm(request.POST or None, instance=task)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(f'/tests/test/{task.id}/')
        return render(request, 'tests/test_edit.html', {'test': task, 'form': form, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    except Task.DoesNotExist:
        return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def reuslt(request, id):
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

    quiz = get_object_or_404(Task, id=id)
    rusults = Result.objects.filter(test=quiz)
    return render(request, 'tests/results.html', {'quiz':quiz, "results":rusults, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})