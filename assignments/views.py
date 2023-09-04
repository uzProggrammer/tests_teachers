from django.shortcuts import render, get_object_or_404
from .models import Assignment, StudentAnswer, StudentAnswerComments, StudentAnswerBall
from django.core.paginator import Paginator
from users.models import MyUser
from django.http import HttpResponseRedirect
from .forms import EditForm
from django.utils import timezone
from django.contrib import messages


def all_assignments(request):
    assignments = Assignment.objects.all().order_by('-date_created')
    object = Paginator(assignments, 40)
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

    if 'page' in request.GET:
        object = object.page(request.GET['page'])
    else:
        object = object.page(1)
    return render(request, 'assignments/assignments.html', {'assignments': assignments, 'object': object, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def assignment_view(request, id):
    unread_assign = None
    unread_answerca2 = []

    assignment = get_object_or_404(Assignment, id=id)
    users = MyUser.objects.all()
    answerca = StudentAnswer.objects.filter(assignment=assignment)
    topshirgan = False
    tugadi =True
    if timezone.now() < assignment.qachongacha:
        tugadi = False
    if request.user.is_authenticated:
        try:
            topshirgan = StudentAnswer.objects.get(student=request.user, assignment=assignment)
            topshirgan = True
        except StudentAnswer.DoesNotExist:
            topshirgan = False
        except StudentAnswer.MultipleObjectsReturned:
            pass
        unread_assign = Assignment.objects.filter(is_readed=False, student=request.user)

        unread_answerca = StudentAnswer.objects.filter(is_readed=False)
        unread_answerca2 = []
        for unread_answerca1 in unread_answerca:

            if unread_answerca1.assignment.author == request.user:
                a = unread_answerca1
                unread_answerca2.append(a)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'ball' in request.POST and request.user == assignment.author:
                ball = request.POST['ball']
                if float(ball) > assignment.max_ball:
                    ball = assignment.max_ball
                xatolar = request.POST['xatolar']
                student_answer_id = request.POST['student_answer_id']
                student_answer = StudentAnswer.objects.get(id=student_answer_id)
                user = MyUser.objects.get(username=student_answer.student.username)
                user.ball += float(ball)
                user.save()
                StudentAnswerBall(teacher=request.user,ball=float(ball),xatolar_va_kamchiliklar=xatolar,student_answer=student_answer).save()
                return HttpResponseRedirect(f'/assignments/assignment/{id}/')
            if request.user.sinf == assignment.sinf or request.user == assignment.student:
                if 'answer' in request.POST:
                    answer = request.POST['answer']
                    if 'helper_users' in request.POST:
                        yordamcila = request.POST.getlist('helper_users')
                        users = []
                        for yordamci in yordamcila:
                            user = MyUser.objects.get(id=int(yordamci))
                            users.append(user)
                    try:
                        StudentAnswer.objects.get(assignment=assignment,student=request.user)
                        salom = True
                    except:
                        salom = False
                    if salom:
                        pass
                    else:
                        student_answer = StudentAnswer.objects.create(assignment=assignment,student=request.user,answer=answer)
                        topshirgan = True
                        for user in users:
                            student_answer.yordam_berganlar.add(user)

                    return HttpResponseRedirect(f'/assignments/assignment/{id}/')
            elif request.user.is_authenticated and 'comment_body' in request.POST:
                comment_body = request.POST['comment_body']
                student_answer = request.POST['student_answer']
                student_answer = StudentAnswer.objects.get(id=int(student_answer))
                StudentAnswerComments(student_answer=student_answer,user=request.user,body=comment_body).save()
                return HttpResponseRedirect(f'/assignments/assignment/{id}/')
        else:
            return render(request, '403.html', status=403)
    if request.user.is_authenticated:
        if request and request.user.is_teacher:
            answers = assignment.assigment_answer.filter(is_readed=False)
            for answer in answers:
                answer.is_readed = True
                answer.save()
        if request and assignment.student==request.user or assignment.sinf == request.user.sinf:
            assignment.is_readed = True
        student_answers = assignment.assigment_answer.all()
        student_answers1 =[]
        for s_a in student_answers:
            student_answers1.append(s_a.student.username)
        return render(request, 'assignments/assignment.html', {'assignment': assignment, 'users': users, 'answerca': answerca,'topshirgan':topshirgan, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2), 'student_answers': student_answers, 'tugadi':tugadi, 'student_answers1': student_answers1, })
    else:
        messages.error(request, 'Siz Dars bo\'limiga o\'tishingiz uchun tizimga kirishingiz shart!')
        return HttpResponseRedirect('/users/login/')

def add_comment_like(request, id):
    if request.user.is_authenticated:
        comment = StudentAnswerComments.objects.get(id=id)
        answerca = comment.student_answer
        assign = answerca.assignment
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        return HttpResponseRedirect(f'/assignments/assignment/{assign.id}/')
    else:
        return render(request, '404.html')

def add_answer_like(request, id):
    if request.user.is_authenticated:
        answer = StudentAnswer.objects.get(id=id)
        assign = answer.assignment
        if request.user in answer.likes.all():
            answer.likes.remove(request.user)
        else:
            answer.likes.add(request.user)
        return HttpResponseRedirect(f'/assignments/assignment/{assign.id}/')

def add_assignment(request):
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
        if request.user.is_teacher or request.user.is_staff:
            last = Assignment.objects.last()
            users = MyUser.objects.filter(is_student=True)
            if request.method == 'POST':
                title = request.POST['title']
                info = request.POST['info']
                sinf = None
                student = None
                student_username = None
                if request.POST['sinf'] != '':
                    sinf = request.POST['sinf']
                if request.POST['student'] != '':
                    student_username = request.POST['student']
                if student_username:
                    student = MyUser.objects.get(id=student_username)
                qachongacha = request.POST['qachongacha']
                max_ball = request.POST['max_ball']

                last = Assignment.objects.create(title=title, info=info,sinf=sinf,student=student,qachongacha=qachongacha, author=request.user, max_ball=max_ball)
                return HttpResponseRedirect(f'/assignments/assignment/{last.id}/')
            return render(request, 'assignments/add.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2), 'users':users})
        else:
            return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    else:
        return render(request, '403.html', status=403)

def edit(request, id):
    ass = get_object_or_404(Assignment, id=id)
    if request.user.is_authenticated:
        if request.user.is_teacher or request.user.is_staff:
            last = Assignment.objects.last()
            users = MyUser.objects.filter(is_student=True)
            if request.method == 'POST':
                title = request.POST.get('title', None)
                ass.title = title

                info = request.POST['info']
                ass.info = info
                sinf = None
                student = None
                student_username = None
                if request.POST['sinf'] != '':
                    sinf = request.POST['sinf']
                ass.sinf = sinf
                if request.POST['student'] != '':
                    student_username = request.POST['student']
                if student_username:
                    student = MyUser.objects.get(id=student_username)
                ass.student = student
                qachongacha = request.POST['qachongacha']
                ass.qachongacha = qachongacha
                max_ball = request.POST['max_ball']
                ass.max_ball=max_ball
                ass.safe()
                return HttpResponseRedirect(f'/assignments/assignment/{ass.id}/')
            return render(request, 'assignments/edit.html', {'users':users, 'ass': ass})
        else:
            return render(request, '404.html', status=404)
    else:
        return render(request, '403.html', status=403)