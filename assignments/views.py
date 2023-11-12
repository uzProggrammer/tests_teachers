from django.shortcuts import render, get_object_or_404
from .models import Assignment, StudentAnswer, StudentAnswerComments, StudentAnswerBall
from django.core.paginator import Paginator
from users.models import MyUser
from django.http import HttpResponseRedirect
from .forms import EditForm
from django.utils import timezone
from django.contrib import messages
from sinflar.models import Sinf
from django.db.models import Q

def all_assignments(request):
    if request.user.is_authenticated and request.user.is_teacher:
        assignments = Assignment.objects.all().order_by('-date_created')
        search = ''
        if 'search' in request.GET:
            search = request.GET.get('search')
        assignments = Assignment.objects.filter(Q(title__icontains=search) | Q(info__icontains=search)).order_by('-date_created')
        assignments = Paginator(assignments, 20)
        if 'page' in request.GET:
            object = assignments.page(request.GET.get('page'))
        else:
            object = assignments.page(1)
        return render(request, 'assignments/assignments.html', {'object': assignments, 'page_obj': object, 'search':search})
    elif request.user.is_authenticated:
        assignments = Assignment.objects.filter(sinf=request.user.sinf).order_by('-date_created')
        search = ''
        if 'search' in request.GET:
            search = request.GET.get('search')
        assignments = Assignment.objects.filter(Q(title__icontains=search) | Q(info__icontains=search), sinf=request.user.sinf).order_by('-date_created')
        assignments = Paginator(assignments, 20)
        if 'page' in request.GET:
            object = assignments.page(request.GET.get('page'))
        else:
            object = assignments.page(1)
        return render(request, 'assignments/assignments.html', {'object': assignments, 'page_obj': object, 'search':search})
    else:
        messages.error(request, 'Ushbu amalni bajarish uchun tizimga kirishingiz kerak!')
        return HttpResponseRedirect('/users/login/')

def assignment_view(request, id):
    # unread_assign = None
    # unread_answerca2 = []

    # assignment = get_object_or_404(Assignment, id=id)
    # users = MyUser.objects.all()
    # answerca = StudentAnswer.objects.filter(assignment=assignment)
    # topshirgan = False
    # tugadi =True
    # if timezone.now() < assignment.qachongacha:
    #     tugadi = False
    # if request.user.is_authenticated:
    #     try:
    #         topshirgan = StudentAnswer.objects.get(student=request.user, assignment=assignment)
    #         topshirgan = True
    #     except StudentAnswer.DoesNotExist:
    #         topshirgan = False
    #     except StudentAnswer.MultipleObjectsReturned:
    #         pass
    #     unread_assign = Assignment.objects.filter(is_readed=False, student=request.user)

    #     unread_answerca = StudentAnswer.objects.filter(is_readed=False)
    #     unread_answerca2 = []
    #     for unread_answerca1 in unread_answerca:

    #         if unread_answerca1.assignment.author == request.user:
    #             a = unread_answerca1
    #             unread_answerca2.append(a)

    # if request.method == 'POST':
    #     if request.user.is_authenticated:
    #         if 'ball' in request.POST and request.user == assignment.author:
    #             ball = request.POST['ball']
    #             if float(ball) > assignment.max_ball:
    #                 ball = assignment.max_ball
    #             xatolar = request.POST['xatolar']
    #             student_answer_id = request.POST['student_answer_id']
    #             student_answer = StudentAnswer.objects.get(id=student_answer_id)
    #             user = MyUser.objects.get(username=student_answer.student.username)
    #             user.ball += float(ball)
    #             user.save()
    #             StudentAnswerBall(teacher=request.user,ball=float(ball),xatolar_va_kamchiliklar=xatolar,student_answer=student_answer).save()
    #             return HttpResponseRedirect(f'/assignments/assignment/{id}/')
    #         if request.user.sinf == assignment.sinf or request.user == assignment.student:
    #             if 'answer' in request.POST:
    #                 answer = request.POST['answer']
    #                 if 'helper_users' in request.POST:
    #                     yordamcila = request.POST.getlist('helper_users')
    #                     users = []
    #                     for yordamci in yordamcila:
    #                         user = MyUser.objects.get(id=int(yordamci))
    #                         users.append(user)
    #                 try:
    #                     StudentAnswer.objects.get(assignment=assignment,student=request.user)
    #                     salom = True
    #                 except:
    #                     salom = False
    #                 if salom:
    #                     pass
    #                 else:
    #                     student_answer = StudentAnswer.objects.create(assignment=assignment,student=request.user,answer=answer)
    #                     topshirgan = True
    #                     for user in users:
    #                         student_answer.yordam_berganlar.add(user)

    #                 return HttpResponseRedirect(f'/assignments/assignment/{id}/')
    #         elif request.user.is_authenticated and 'comment_body' in request.POST:
    #             comment_body = request.POST['comment_body']
    #             student_answer = request.POST['student_answer']
    #             student_answer = StudentAnswer.objects.get(id=int(student_answer))
    #             StudentAnswerComments(student_answer=student_answer,user=request.user,body=comment_body).save()
    #             return HttpResponseRedirect(f'/assignments/assignment/{id}/')
    #     else:
    #         return render(request, '403.html', status=403)
    # if request.user.is_authenticated:
    #     if request and request.user.is_teacher:
    #         answers = assignment.assigment_answer.filter(is_readed=False)
    #         for answer in answers:
    #             answer.is_readed = True
    #             answer.save()
    #     if request and assignment.student==request.user or assignment.sinf == request.user.sinf:
    #         assignment.is_readed = True
    #     student_answers = assignment.assigment_answer.all()
    #     student_answers1 =[]
    #     for s_a in student_answers:
    #         student_answers1.append(s_a.student.username)
    #     return render(request, 'assignments/assignment.html', {'assignment': assignment, 'users': users, 'answerca': answerca,'topshirgan':topshirgan, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2), 'student_answers': student_answers, 'tugadi':tugadi, 'student_answers1': student_answers1, })

    if request.user.is_authenticated:
        assignment = get_object_or_404(Assignment, id=id)
        now = timezone.now()
        if request.method == 'POST':
            if request.user.sinf == assignment.sinf:
                if 'answer' in request.POST:
                    answer = request.POST.get('answer')
                    try:
                        s_answer = StudentAnswer.objects.get(assignment=assignment, student=request.user)
                        return HttpResponseRedirect(f'/assignments/assignment/{assignment.id}/')
                    except StudentAnswer.DoesNotExist:
                        s_answer = StudentAnswer.objects.create(assignment=assignment, student=request.user, answer=answer)
                        assignment.javoblar.add(request.user)
                        messages.success(request, 'Javobingiz tizimga qo\'shildi. Tezorada o\'qituvchilar tomonidan tekshirilib ball beriladi.')
                        return HttpResponseRedirect(f'/assignments/assignment/{assignment.id}/')
                else:
                    return HttpResponseRedirect(f'/assignments/assignment/{assignment.id}/')
            else:
                messages.error(request, 'Ushbu darsga siz javobb berishingiz mumkin emas!')
                return HttpResponseRedirect(f'/assignments/assignment/{assignment.id}/')
        return render(request, 'assignments/assignment.html', {'assignment':assignment, 'now':now})
    else:
        messages.error(request, 'Siz Dars bo\'limiga o\'tishingiz uchun tizimga kirishingiz shart!')
        return HttpResponseRedirect('/users/login/')

def my_answer(request, id):
    if request.user.is_authenticated:
        assignment = get_object_or_404(Assignment, id=id)
        if request.user in assignment.javoblar.all():
            s_answer = StudentAnswer.objects.get(assignment=assignment, student=request.user)
            return render(request, 'assignments/my-a.html', {'assignment': assignment, 's_answer':s_answer})
    else:
        messages.error(request, 'Siz ushbu bo\'limiga o\'tishingiz uchun tizimga kirishingiz shart!')
        return HttpResponseRedirect('/users/login/')

def ballar(request, id):
    if request.user.is_authenticated:
        assignment = get_object_or_404(Assignment, id=id)
        balls = StudentAnswerBall.objects.filter(assignment=assignment).order_by('-ball')
        return render(request, 'assignments/balls.html', {'assignment': assignment, 'balls':balls})
    else:
        messages.error(request, 'Siz ushbu bo\'limiga o\'tishingiz uchun tizimga kirishingiz shart!')
        return HttpResponseRedirect(f'/assignments/assignment/{assignment.id}/')

def answers(request, id):
    if request.user.is_authenticated:
        assignment = get_object_or_404(Assignment, id=id)
        if request.user.is_staff or request.user.is_teacher or request.user.is_create_ass or assignment.qachongacha<timezone.now():
            answers = StudentAnswer.objects.filter(assignment=assignment).order_by('-date_created')

            return render(request, 'assignments/answers.html', {'assignment': assignment, 'answers':answers})
        messages.error(request, 'Ushbu bo\'limga kirishiingiz mumkin emas')
        return HttpResponseRedirect('/users/login/')
    else:
        messages.error(request, 'Siz ushbu bo\'limiga o\'tishingiz uchun tizimga kirishingiz shart!')
        return HttpResponseRedirect('/users/login/')

def answer(request, id, id1):
    if request.user.is_authenticated:
        assignment = get_object_or_404(Assignment, id=id)
        if request.user.is_staff or request.user.is_teacher or request.user.is_create_ass or assignment.qachongacha<timezone.now():
            answer = get_object_or_404(StudentAnswer, assignment=assignment, id=id1)
            if request.method == 'POST':
                if answer.student_answer_ball.count()==0:
                    ball = request.POST.get('ball')
                    if float(ball) > assignment.max_ball:
                        ball = assignment.max_ball
                    user = MyUser.objects.get(username=answer.student.username)
                    user.ball += float(ball)
                    user.save()
                    StudentAnswerBall(teacher=request.user,ball=float(ball),student_answer=answer,assignment=assignment).save()
                    return HttpResponseRedirect(f'/assignments/assignment/{id}/answers/{id1}/')
                else:
                    messages.error(request, f'Bu o\'quvchi allaqochon {answer.student_answer_ball.first().ball} ball olib bo\'lgan')
                    return HttpResponseRedirect('/assignments/assignment/{id}/answers/{id1}/')

            return render(request, 'assignments/answer.html', {'assignment': assignment, 'answer':answer})
        messages.error(request, 'Ushbu bo\'limga kirishiingiz mumkin emas')
        return HttpResponseRedirect('/users/login/')
    else:
        messages.error(request, 'Siz ushbu bo\'limiga o\'tishingiz uchun tizimga kirishingiz shart!')
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
        sinflar = Sinf.objects.all().order_by('nom')
        if request.user.is_teacher or request.user.is_staff or request.user.is_create_ass:
            last = Assignment.objects.last()
            users = MyUser.objects.filter(is_student=True)
            if request.method == 'POST':
                title = request.POST.get('title')
                info = request.POST.get('info')
                sinf = None
                if request.POST['sinf'] != '':
                    sinf = request.POST.get('sinf')
                qachongacha = request.POST.get('qachongacha')
                max_ball = request.POST.get('max_ball')

                last = Assignment.objects.create(title=title, info=info,sinf=sinf,qachongacha=qachongacha, author=request.user, max_ball=max_ball)
                return HttpResponseRedirect(f'/assignments/assignment/{last.id}/')
            return render(request, 'assignments/add.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2), 'users':users, 'sinflar':sinflar})
        else:
            return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    else:
        return render(request, '403.html', status=403)

def delete(request, id):
    ass = get_object_or_404(Assignment, id=id)
    if request.user.is_staff or request.user.is_teacher or request.user.is_create_ass:
        if request.method=='POST':
            ass.delete()
            messages.success(request, 'Dars muvaffaqiyatli o\'chirib tashlandi!')
            return HttpResponseRedirect(f'/assignments/')
        return render(request, 'assignments/delete.html', {'assignment':ass})
    else:
        messages.error(request, 'Ushbu bo\'limga o\'tishingiz mumkin emas!')
        return render(request, '403.html', status=403)

def edit(request, id):
    ass = get_object_or_404(Assignment, id=id)
    sinflar = Sinf.objects.all().order_by('nom')
    if request.user.is_authenticated:
        if request.user.is_teacher or request.user.is_staff or request.user.is_create_ass:
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
                qachongacha = request.POST['qachongacha']
                ass.qachongacha = qachongacha
                max_ball = request.POST['max_ball']
                ass.max_ball=max_ball
                ass.save()
                return HttpResponseRedirect(f'/assignments/assignment/{ass.id}/')
            return render(request, 'assignments/edit.html', {'users':users, 'ass': ass, 'sinflar':sinflar})
        else:
            return render(request, '404.html', status=404)
    else:
        return render(request, '403.html', status=403)