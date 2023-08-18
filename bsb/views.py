import json

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from assignments.models import Assignment
from problems.complier import Complier
from sinflar.models import Sinf
from users.models import MyUser
from .forms import EditForm, AttemptForm
from .models import BSB, BsbAssignment, StudentAnswer, StudentAnswerBall, BsbProblem, BsbProblemAnswer, BsbProblemBall, \
    BsbQuiz, BsbQuizTests, BsbQuizBall, Yakuniy
from django.utils import timezone

def all_bsb(request):
    bsbs = BSB.objects.all().order_by('-id')
    return render(request, 'bsb/al_bsb.html', {'bsbs':bsbs})

def edit_bsb(request, id):
    bsb = get_object_or_404(BSB, id=id)
    if request.user.is_staff or request.user.is_teacher or request.user.is_superuser:
        sinflar = Sinf.objects.all().order_by('nom')
        if request.method == 'POST':
            info = request.POST['info']
            sinf_id = int(request.POST['sinf'])
            sinf = Sinf.objects.get(id=sinf_id)
            type = request.POST['type']
            d_end = request.POST['d_end']
            d_start = request.POST['d_start']
            title = request.POST['title']
            bsb.body = info
            bsb.sinf = sinf
            bsb.type = type
            bsb.date_ended = d_end
            bsb.date_statrted = d_start
            bsb.title = title
            bsb.save()
            return HttpResponseRedirect(f'/controls/control/{id}/')
        return render(request, 'bsb/bsb_edit.html', {'bsb':bsb, 'sinflar':sinflar})
    else:
        return render(request, '404.html')

def add_bsb(request):
    if request.user.is_staff or request.user.is_teacher or request.user.is_superuser:
        sinflar = Sinf.objects.all().order_by('nom')
        if request.method == 'POST':
            info = request.POST['info']
            sinf_id = request.POST['sinf']
            sinf = Sinf.objects.get(nom=sinf_id)
            type = request.POST['type']
            d_end = request.POST['d_end']
            d_start = request.POST['d_start']
            title = request.POST['title']
            bsb = BSB.objects.create(body=info, sinf=sinf,type=type,date_ended=d_end,date_statrted=d_start, title=title, author=request.user)
            return HttpResponseRedirect(f'/controls/control/{bsb.id}/')
        return render(request, 'bsb/bsb_add.html', {'sinflar': sinflar})
    else:
        return render(request, '404.html')

def bsb_view(request, id):
    bsb = get_object_or_404(BSB, id=id)
    davomiylig = bsb.date_ended - bsb.date_statrted
    dovom_etmoqda = False
    tugagan = False
    is_userca = False
    if timezone.now() > bsb.date_statrted and timezone.now() < bsb.date_ended:
        bsb.holati = 'Dovom etmoqda'
        bsb.save()
        dovom_etmoqda = True
    elif timezone.now() > bsb.date_ended:
        tugagan = True
        bsb.holati = 'Tugagan'
        bsb.save()
    elif timezone.now() < bsb.date_statrted:
        bsb.holati = 'Boshlanmagan'
        bsb.save()
    if request.user.is_authenticated:
        if request.user.sinf == bsb.sinf.nom and timezone.now() > bsb.date_statrted and timezone.now() < bsb.date_ended:
            is_userca = True
        return render(request, 'bsb/bsb.html', {'bsb':bsb, 'davomiylig':davomiylig, 'dovom_etmoqda':dovom_etmoqda, 'tugagan':tugagan, 'is_userca':is_userca})
    return render(request, 'bsb/bsb.html', {'bsb':bsb, 'davomiylig':davomiylig, 'dovom_etmoqda':dovom_etmoqda, 'tugagan':tugagan,})

def bsb_assignments(request, id):
    bsb = get_object_or_404(BSB, id=id)
    if bsb.type == 'Topshiriq':
        if request.user.is_authenticated:
            if timezone.now() > bsb.date_statrted and timezone.now() < bsb.date_ended and request.user.sinf == bsb.sinf.nom and bsb.type=='Topshiriq' or request.user.is_staff or request.user == bsb.author:
                return render(request, 'bsb/bsb_assignments.html', {'bsb':bsb})
            else:
                return HttpResponseRedirect(f'/controls/control/{bsb.id}')
        else:
            return render(request, 'bsb/bsb_assignments.html', {'bsb':bsb})
    else:
        return HttpResponseNotFound()

def bsb_assignment(request, id, id1):
    bsb = get_object_or_404(BSB, id=id)
    if bsb.type == 'Topshiriq':
        if request.user.is_authenticated:
            if timezone.now() > bsb.date_statrted and timezone.now() < bsb.date_ended and request.user.sinf == bsb.sinf.nom and bsb.type == 'Topshiriq' or request.user.is_staff or request.user == bsb.author:


                assignment = get_object_or_404(BsbAssignment, id=id1)
                users = MyUser.objects.all()
                answerca = StudentAnswer.objects.filter(assignment=assignment)


                if request.method == 'POST':
                    if 'ball' in request.POST and request.user == assignment.author or request.user.is_staff:
                        ball = request.POST['ball']
                        if float(ball) > assignment.ball:
                            ball = assignment.ball
                        student_answer_id = request.POST['student_answer_id']
                        student_answer = StudentAnswer.objects.get(id=student_answer_id)
                        user = MyUser.objects.get(username=student_answer.user.username)
                        user.ball += float(ball)
                        user.save()
                        StudentAnswerBall(ball=float(ball),
                                        student_answer=student_answer, user=student_answer.user, bsb=bsb).save()
                        ball1 = 0
                        for i in student_answer.answer_balls.all():
                            ball1+=i.ball
                        yakuniy = Yakuniy.objects.get_or_create(bsb=bsb, user=student_answer.user)
                        yakuniy[0].ball = ball1
                        yakuniy[0].assignments.add(assignment)
                        yakuniy[0].save()
                        return HttpResponseRedirect(f'/controls/control/{id}/assignments/assignment/{id1}/')
                    if request.user.sinf == bsb.sinf.nom:
                        if 'answer' in request.POST:
                            answer = request.POST['answer']

                            try:
                                StudentAnswer.objects.get(assignment=assignment, user=request.user)
                                salom = True
                            except:
                                salom = False
                            if salom:
                                pass
                            else:
                                student_answer = StudentAnswer.objects.create(assignment=assignment, user=request.user,
                                                                            body=answer)
                            return HttpResponseRedirect(f'/controls/control/{id}/assignments/assignment/{id1}/')
                student_answers = assignment.answers.all()
                student_answers1 = []
                for s_a in student_answers:
                    student_answers1.append(s_a.user.username)
                return render(request, 'bsb/bsb_assignment.html',
                            {'bsb':bsb, 'assignment': assignment, 'users': users, 'answerca': answerca,
                            'student_answers': student_answers, 'student_answers1': student_answers1, })
            else:
                return HttpResponseRedirect(f'/controls/control/{bsb.id}')
        else:
            assignment = get_object_or_404(BsbAssignment, id=id1)
            if timezone.now() < bsb.date_ended:
                assignment = get_object_or_404(BsbAssignment, id=id1)
                if request.method == 'POST':
                    return HttpResponseForbidden()
            return render(request, 'bsb/bsb_assignments.html', {'bsb':bsb, 'assignment': assignment})
    else:
        return HttpResponseNotFound()

def add_bsb_assignment(request, id):
    bsb = get_object_or_404(BSB, id=id)
    if (request.user.is_teacher or request.user.is_staff) and bsb.type == 'Topshiriq':
        last = BsbAssignment.objects.last()
        users = MyUser.objects.filter(is_student=True)
        if request.method == 'POST' and bsb.type == 'Topshiriq':
            title = request.POST['title']
            info = request.POST['info']
            max_ball = request.POST['max_ball']

            ass = BsbAssignment.objects.create(title=title, info=info, author=request.user, ball=max_ball, Bsb=bsb)
            return HttpResponseRedirect(f'/controls/control/{id}/assignments/assignment/{ass.id}/')
        return render(request, 'bsb/bsb_add_assignment.html', {'users':users, 'bsb':bsb})
    else:
        return render(request, '404.html',)

def edit_bsb_assignment(request, id, id1):
    bsb = get_object_or_404(BSB, id=id)
    ass = get_object_or_404(BsbAssignment, id=id1)
    form = EditForm(request.POST or None, instance=ass)
    if request.method == 'POST' and request.user.is_staff or request.user.is_teacher and bsb.type == 'Topshiriq':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/controls/control/{id}/assignments/assignment/{id1}/')
    return render(request, 'assignments/edit.html', {'form': form, 'bsb':bsb})

def add_answer_ball(request, id, id1):
    bsb = get_object_or_404(BSB, id=id)
    if request.user.is_staff or request.user.is_teacher  and bsb.type == 'Topshiriq':
        student_answer = get_object_or_404(StudentAnswer, id=id1)
        if request.method=='POST':
            ball = float(request.POST.get('ball'))
            if float(ball) > student_answer.assignment.ball:
                ball = student_answer.assignment.ball
            ball = StudentAnswerBall.objects.create(ball=ball, student_answer=student_answer, user=student_answer.user, bsb=bsb)
            ball1 = 0
            for i in student_answer.answer_balls.all():
                ball1 += i.ball
            yakuniy = Yakuniy.objects.get_or_create(bsb=bsb, user=student_answer.user)
            yakuniy[0].ball = ball1
            yakuniy[0].assignments.add(ball.student_answer.assignment)
            yakuniy[0].save()
            return HttpResponseRedirect(f'/controls/control/{id}/results/')
        return render(request, 'bsb/student_answer.html', {'student_answer': student_answer, 'bsb': bsb})
    else:
        return render(request, '404.html')

def bsb_problems(request, id):
    bsb = get_object_or_404(BSB, id=id)
    if timezone.now() > bsb.date_statrted and timezone.now() < bsb.date_ended and request.user.sinf == bsb.sinf.nom and bsb.type=='Masala' or request.user.is_staff or request.user == bsb.author:
        problems = bsb.problems.all()
        return render(request, 'bsb/bsb_problems.html', {'bsb':bsb, 'problems':problems})
    else:
        return HttpResponseRedirect(f'/controls/control/{id}')

def bsb_problem(request, id, id1):
    bsb = get_object_or_404(BSB, id=id)
    if bsb.type == 'Masala':
        unread_assign = None
        unread_answerca2 = []
        if request.user.is_authenticated:
            unread_assign = Assignment.objects.filter(is_readed=False, student=request.user)
            unread_answerca2 = []


        task = get_object_or_404(BsbProblem, id=id1)
        task_attempts = None
        formca = None
        if request.user.sinf == bsb.sinf.nom:
            attemptca = BsbProblemAnswer.objects.filter(bsb_problem=task, user=request.user).last()
            formca = AttemptForm(request.POST or None, instance=attemptca)
            task_attempts = BsbProblemAnswer.objects.filter(user=request.user, bsb_problem=task).order_by('-id')
        task_attempts1 = BsbProblemAnswer.objects.filter(bsb_problem=task).order_by('-id')
        if request.method == 'POST' and bsb.type == 'Masala' and request.user.sinf == bsb.sinf.nom:
            if request.user.is_teacher or request.user.is_staff:
                if 'body' in request.POST:
                    runner = Complier(body=request.POST['body'], time_limit=task.time_limit * 5,
                                      memory_limit=task.memory_limit,
                                      tests=task.tests)
                    data = runner.run()
                    if data['status'] == 'Accepted':
                        messages.success(request, f'Accepted')
                        return HttpResponseRedirect(f'/controls/control/{id}/problems/problem/{id1}/')
                    else:
                        messages.danger(request, f'{data["status"]}')
                        return HttpResponseRedirect(f'/controls/control/{id}/problems/problem/{id1}/')
            if request.user.is_authenticated and request.user.sinf == bsb.sinf.nom:

                if 'body' in request.POST:
                    runner = Complier(body=request.POST['body'], time_limit=task.time_limit*5, memory_limit=task.memory_limit,
                                      tests=task.tests)
                    data = runner.run()
                    problem_answer = BsbProblemAnswer.objects.create(bsb_problem=task, user=request.user, body=request.POST['body'], type=data['status'])
                    if data['status'] == 'Accepted':
                        task.accepteds.add(request.user)
                        try:
                            ball = BsbProblemBall.objects.get(bsb_problem_answer=problem_answer,
                                                                 user=problem_answer.user)
                            ball1 = 0
                            for i in problem_answer.balls.all():
                                ball1 += i.ball
                            yakuniy = Yakuniy.objects.get_or_create(bsb=bsb,
                                                                    user=problem_answer.user)
                            yakuniy[0].ball += ball1
                            yakuniy[0].problem.add(task)
                            yakuniy[0].save()
                            messages.success(request, f'Siz bu masaladan {ball} ball olgansiz')
                        except BsbProblemBall.DoesNotExist:
                            try:
                                wrong_answers = BsbProblemAnswer.objects.filter(user=problem_answer.user,
                                                                                bsb_problem=task).exclude(type='Accepted')
                            except:
                                wrong_answers = []
                            jarima = len(wrong_answers) * 0
                            ballca = task.ball - jarima

                            ball = BsbProblemBall.objects.create(bsb_problem_answer=problem_answer,
                                                                 user=problem_answer.user, ball=ballca)
                            ball1 = 0
                            for i in problem_answer.balls.all():
                                ball1 += i.ball
                            yakuniy = Yakuniy.objects.get_or_create(bsb=bsb,
                                                                    user=problem_answer.user)
                            yakuniy[0].ball = ball1
                            yakuniy[0].problem.add(task)
                            yakuniy[0].save()
                            messages.success(request, f'Siz {task.ball} balldan {ball.ball} ball oldingiz')
                    else:
                        if request.user in task.accepteds.all():
                            pass
                        else:
                            task.wrong_answers.add(request.user)

                    return HttpResponseRedirect(f'/controls/control/{id}/problems/problem/{id1}/')
            else:
                return render(request, '404.html')

        return render(request, 'bsb/bsb_problem.html',
                      {'task': task, 'task_attempts': task_attempts, 'task_attempts1': task_attempts1, 'formca': formca,
                       'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2), 'bsb':bsb})
    else:
        return HttpResponseRedirect(f'controls/control/{id}')

def edit_bsb_problem(request, id, id1):
    bsb = get_object_or_404(BSB, id=id)
    if request.user.is_staff or request.user.is_teacher and bsb.type == 'Masala':
        problem = get_object_or_404(BsbProblem, id=id1)
        simple_t = json.dumps(problem.simple_tests)
        tests = json.dumps(problem.tests)
        if request.method == 'POST':
            title = request.POST['title']
            problem.title = title
            diff = int(request.POST.get('diff', False))
            problem.difficulty = diff
            tl = int(request.POST.get('tl', False))
            problem.time_limit = tl
            ml = int(request.POST.get('ml', False))
            problem.memory_limit = ml
            about = request.POST.get('about', False)
            problem.about = about
            in_ = request.POST.get('in_', False)
            problem.info_in = in_
            out = request.POST.get('out', False)
            problem.info_out = out
            try:
                st = json.loads(request.POST.get('st', False))
            except:
                messages.error(request, 'Siz kiritgan simple testlar JSON formatida emas')
                return render(request, 'bsb/add_problem.html', {'bsb': bsb})
            problem.simple_tests = st
            try:
                t = json.loads(request.POST.get('tests', False))
            except:
                messages.error(request, 'Siz kiritgan testlar JSON formatida emas')
                return render(request, 'bsb/add_problem.html', {'bsb': bsb})
            problem.tests = t
            yechim = request.POST.get('yechim', False)
            problem.yechim = yechim
            problem.save()
            return HttpResponseRedirect(f'/controls/control/{id}/problems/problem/{id1}/')
        return render(request, 'bsb/bsb_problem_edit.html', {'bsb':bsb, 'problem':problem, 'simple_t': simple_t, 'tests':tests})
    else:
        return HttpResponseRedirect(request, '404.html')

def get_attempt(request, id, id1):
    bsb = get_object_or_404(BSB, id=id)
    if request.user.is_teacher or request.user.is_staff and bsb.type == 'Masala':
        attempt = get_object_or_404(BsbProblemAnswer, id=id1)
        return render(request, 'bsb/attempt.html', {'attempt':attempt, 'bsb':bsb})
    else:
        return render(request, '404.html')

def add_bsb_problem(request, id):
    bsb = get_object_or_404(BSB, id=id)
    if request.user.is_teacher or request.user.is_staff and bsb.type == 'Masala':
        if request.method == 'POST':
            title = request.POST['title']
            diff = int(request.POST.get('diff', False))
            tl = int(request.POST.get('tl', False))
            ml = int(request.POST.get('ml', False))
            about = request.POST.get('about', False)
            in_ = request.POST.get('in_', False)
            out = request.POST.get('out', False)
            try:
                st = json.loads(request.POST.get('st', False))
            except:
                messages.error(request, 'Siz kiritgan simple testlar JSON formatida emas')
                return render(request, 'bsb/add_problem.html', {'bsb': bsb})
            try:
                t = json.loads(request.POST.get('tests', False))
            except:
                messages.error(request, 'Siz kiritgan testlar JSON formatida emas')
                return render(request, 'bsb/add_problem.html', {'bsb': bsb})
            yechim = request.POST.get('yechim', False)
            ball = float(request.POST.get('ball', False))
            problem = BsbProblem.objects.create(title=title,
                                                difficulty=diff, time_limit=tl, memory_limit=ml,
                                                about=about,info_out=out, info_in=in_,
                                                simple_tests=st, tests=t, yechim=yechim, ball=ball, user=request.user, bsb=bsb)
            return HttpResponseRedirect(f'/controls/control/{id}/problems/problem/{problem.id}/')
        return render(request, 'bsb/add_problem.html', {'bsb':bsb})
    else:
        return render(request, '404.html')


def bsb_quizess(request, id):
    bsb = get_object_or_404(BSB, id=id)
    if request.user.sinf == bsb.sinf.nom and bsb.type == 'Test' and not BsbQuizBall.objects.filter(test=bsb, user=request.user).exists() or request.user.is_staff or request.user.is_teacher:
        quizes = bsb.quizess.all()

        return render(request, 'bsb/quizess.html', {'bsb':bsb, 'quizes':quizes})
    else:
        messages.warning(request, 'Siz bu nazorat ishining teslariga allaqachon javob berib bo\'lgansiz')
        return HttpResponseRedirect(f'/controls/control/{bsb.id}/')

def post_bsb_question(request, id):
    bsb = get_object_or_404(BSB, id=id)

    if request.user.sinf == bsb.sinf.nom and bsb.type == 'Test' and not BsbQuizBall.objects.filter(test=bsb, user=request.user).exists():
        if request.method == 'POST':
            data = {}
            data1 = []
            data3 = []
            for key, value in request.POST.items():
                if key != 'csrfmiddlewaretoken':
                    quiz = BsbQuiz.objects.get(id=key)
                    answer = BsbQuizTests.objects.get(id=value)
                    data3.append(answer)
                    if answer.is_true:
                        data[quiz.id] = True
                        data1.append(quiz.ball)
                    else:
                        data[quiz.id] = False
            scope = sum(data1)
            answer = BsbQuizBall.objects.create(test=bsb, scope=scope, user=request.user)
            for values in data3:
                answer.quizess.add(values)
            user = MyUser.objects.get(username=request.user.username)
            user.ball += sum(data1)
            user.save()
            return render(request, 'bsb/quiz_post.html', {'data':data, 'data1':sum(data1), 'bsb':bsb})
        else:
            return HttpResponseRedirect(f'/controls/control/{bsb.id}/')
    else:
        return HttpResponseRedirect(f'/controls/control/{bsb.id}/')

def add_bsb_quiz(request, id):
    bsb = get_object_or_404(BSB, id=id)
    if request.user.is_staff or request.user.is_teacher and bsb.type == 'Test':
        if request.method == 'POST':
            quiz = request.POST
            BsbQuiz(bsb=bsb, body=request.POST.get('quiz-title'), ball=int(request.POST.get('ball'))).save()
            new_answer = BsbQuiz.objects.last()
            is_true = request.POST['is_true']
            for answer_key, answer_value in quiz.items():
                if answer_key == 'csrfmiddlewaretoken' or answer_key == 'quiz-title' or answer_key == 'is_true' or answer_key=='ball':
                    pass
                else:
                    if answer_key.split('-')[-1] == is_true:
                        BsbQuizTests(question=new_answer, body=answer_value, is_true=True).save()
                        continue
                    else:
                        BsbQuizTests(question=new_answer, body=answer_value).save()
                        continue
            messages.success(request, 'Yangi test yaratildi!')
            return HttpResponseRedirect(f'/controls/control/{bsb.id}/')
        return render(request, 'bsb/add_test.html', {'bsb':bsb})
    else:
        return render(request, '404.html')

def quiz_answer(request, id, id1):
    bsb = get_object_or_404(BSB, id=id)
    answer = get_object_or_404(BsbQuizBall, id=id1)
    if request.user == answer.user or request.user.is_staff or request.user.is_teacher and bsb.type == 'Test':
        return render(request, 'bsb/quiz_answer.html', {'bsb':bsb, 'answer': answer})
    else:
        return render(request, '404.html')






def results(request, id):
    bsb = get_object_or_404(BSB, id=id)
    if bsb.type == 'Topshiriq':
        answers = bsb.yakuniy.all()
    elif bsb.type == 'Masala':
        answers = bsb.yakuniy.all()
    else:
        answers = bsb.balls.all()
    return render(request, 'bsb/results.html', {'bsb':bsb, 'answers':answers})