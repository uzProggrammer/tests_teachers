import json

from tracemalloc import is_tracing
from django.shortcuts import render, get_object_or_404
from .models import Course, CourseMultiQuiz, CourseQuiz, CourseQuizVariant, CourseTag, CourseYopiqTest, DragAndDropAnswer, DragAndDropQuiz, DragAndDropVariant, Lectures, Lessons, MultiQuizAnswer, MultiQuizVariuant, QuizAnswer, YopiqTestAnswer
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse, HttpRequest
from django.contrib import messages
import random, string

def create_course(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_teacher:
            if request.method == 'POST':
                body = '...'
                if 'body' in request.POST:
                    body = request.POST.get('body', None)
                course = Course.objects.create(author=request.user, title=request.POST.get('title', None), summary=request.POST.get('summary', None), about=body, )
                if 'teg' in request.POST:
                    for i in request.POST.getlist('teg'):
                        teg = CourseTag.objects.get_or_create(title=i)
                        course.tags.add(teg[0])
                        course.save()
                messages.success(request, 'Muffiqiyatli Kurs yaratildi! ')
                return HttpResponseRedirect(f'/courses/course/{course.id}')
            return render(request, 'courses/create/course.html')
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def create_lesson(request: HttpRequest, id):
    course = get_object_or_404(Course, id=id)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == course.author:
            body = '...'
            if 'body' in request.POST:
                body = request.POST.get('body')

            letters = string.ascii_letters
            digits = string.digits
            all_ch = letters+digits
            pwd_length = 40
            pwd = ''.join(random.sample(all_ch, pwd_length))

            title = request.POST.get('title')
            lesson = Lessons.objects.create(title=title,slug=pwd, summary=body, course=course)
            messages.success(request, 'Dars Kursga muffiqiyatli qo\'shildi')
            if 'url' in request.POST:
                if request.POST.get('url') == 'course':
                    return HttpResponseRedirect(f'/courses/course/{lesson.course.id}/')
                else:
                    return HttpResponseRedirect(f'/courses/course/{lesson.course.id}/lesson/{lesson.slug}/')
            return HttpResponseRedirect(f'/courses/course/{lesson.course.id}/')
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def url_to_create(request: HttpRequest, id, slug):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == course.author:
            if 'type' in request.GET:
                type = request.GET.get('type')
                if type == 'one':
                    return HttpResponseRedirect(f'/courses/course/{id}/lesson/{slug}/add-lecture/')
                elif type == 'two':
                    return HttpResponseRedirect(f'/courses/course/{id}/lesson/{slug}/add-test/')
                elif type == 'three':
                    return HttpResponseRedirect(f'/courses/course/{id}/lesson/{slug}/add-closed-test/')
                elif type == 'four':
                    return HttpResponseRedirect(f'/courses/course/{id}/lesson/{slug}/add-multi-test/')
                elif type == 'five':
                    return HttpResponseRedirect(f'/courses/course/{id}/lesson/{slug}/add-drag-and-drop-test/')
                else:
                    return HttpResponseRedirect(f'/courses/course/{id}/lesson/{slug}/')
            else:
                return HttpResponseRedirect(f'/courses/course/{id}/lesson/{slug}/')
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def create_quiz_view(request: HttpRequest, id, slug):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == course.author:
            if request.method == 'POST':
                quiz = request.POST

                letters = string.ascii_letters
                digits = string.digits
                all_ch = letters+digits
                pwd_length = 40
                pwd = ''.join(random.sample(all_ch, pwd_length))

                new_answer = CourseQuiz.objects.create(lesson=lesson, body=request.POST['quiz-title'], course=course, slug=pwd)
                is_true = int(request.POST['is_true'])
                for answer_key, answer_value in quiz.items():
                    if answer_key == 'csrfmiddlewaretoken' or answer_key == 'quiz-title' or answer_key == 'is_true':
                        pass
                    else:
                        if int(answer_key.split('-')[-1])==is_true:
                            CourseQuizVariant.objects.create(quiz=new_answer, body=answer_value, is_true=True)
                        else:
                            CourseQuizVariant(quiz=new_answer, body=answer_value).save()
                messages.success(request, 'Muffovviqiyatli test tizimga qo\'shildi!')
                return HttpResponseRedirect(f'/courses/course/{course.id}/lesson/{lesson.slug}/quiz/{new_answer.slug}/')
            course_items = course.drag_and_drop_quizes.count() + course.lectures.count() + \
                + course.assignments.count()+course.quizess.count()+course.multi_quizess.count()
            t = 0
            for i in course.drag_and_drop_quizes.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.lectures.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.assignments.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.quizess.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.multi_quizess.all():
                if request.user in i.users.all():
                    t+=1
            answers_count = t
            foiz = 0

            if course_items!=0:
                foiz = round((answers_count/course_items)*100)
            lektures = lesson.lektures.all()
            drag_and_drops = lesson.drag_and_drop.all()
            yopiq_test = lesson.yopiq_tests.all()
            quizess = lesson.quizes.all()
            multi_quizes = lesson.multi_quizes.all()

            return render(request, 'courses/create/quiz.html', {'lesson': lesson, 'course': course, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def create_multiquiz_view(request: HttpRequest, id, slug):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == course.author:
            if request.method == 'POST':
                quiz = request.POST

                letters = string.ascii_letters
                digits = string.digits
                all_ch = letters+digits
                pwd_length = 40
                pwd = ''.join(random.sample(all_ch, pwd_length))

                new_answer = CourseMultiQuiz.objects.create(lesson=lesson, body=request.POST['quiz-title'], course=course, slug=pwd)
                is_true = request.POST.getlist('is_true')
                for answer_key, answer_value in quiz.items():
                    if answer_key == 'csrfmiddlewaretoken' or answer_key == 'quiz-title' or answer_key == 'is_true':
                        pass
                    else:
                        if answer_key.split('-')[-1] in is_true:
                            MultiQuizVariuant.objects.create(quiz=new_answer, body=answer_value, is_true=True)
                        else:
                            MultiQuizVariuant(quiz=new_answer, body=answer_value).save()
                messages.success(request, 'Muffovviqiyatli test tizimga qo\'shildi!')
                return HttpResponseRedirect(f'/courses/course/{course.id}/lesson/{lesson.slug}/multi-quiz/{new_answer.slug}/')
            course_items = course.drag_and_drop_quizes.count() + course.lectures.count() + \
                + course.assignments.count()+course.quizess.count()+course.multi_quizess.count()
            t = 0
            for i in course.drag_and_drop_quizes.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.lectures.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.assignments.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.quizess.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.multi_quizess.all():
                if request.user in i.users.all():
                    t+=1
            answers_count = t
            foiz = 0

            if course_items!=0:
                foiz = round((answers_count/course_items)*100)
            lektures = lesson.lektures.all()
            drag_and_drops = lesson.drag_and_drop.all()
            yopiq_test = lesson.yopiq_tests.all()
            quizess = lesson.quizes.all()
            multi_quizes = lesson.multi_quizes.all()

            return render(request, 'courses/create/multiquiz.html', {'lesson': lesson, 'course': course, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def create_lecture_view(request: HttpRequest, id, slug):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == course.author:
            if request.method == 'POST':
                body = '...'
                if 'body' in request.POST:
                    body = request.POST.get('body')

                letters = string.ascii_letters
                digits = string.digits
                all_ch = letters+digits
                pwd_length = 40
                pwd = ''.join(random.sample(all_ch, pwd_length))

                lecture = Lectures.objects.create(lesson=lesson,course=course, slug=pwd, body=body)
                messages.success(request, 'Muffovviqiyatli Ma\'lumot tizimga qo\'shildi!')
                return HttpResponseRedirect(f'/courses/course/{course.id}/lesson/{lesson.slug}/lecture/{lecture.slug}/')
            course_items = course.drag_and_drop_quizes.count() + course.lectures.count() + \
                + course.assignments.count()+course.quizess.count()+course.multi_quizess.count()
            t = 0
            for i in course.drag_and_drop_quizes.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.lectures.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.assignments.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.quizess.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.multi_quizess.all():
                if request.user in i.users.all():
                    t+=1
            answers_count = t
            foiz = 0

            if course_items!=0:
                foiz = round((answers_count/course_items)*100)
            lektures = lesson.lektures.all()
            drag_and_drops = lesson.drag_and_drop.all()
            yopiq_test = lesson.yopiq_tests.all()
            quizess = lesson.quizes.all()
            multi_quizes = lesson.multi_quizes.all()

            return render(request, 'courses/create/lecture.html', {'lesson': lesson, 'course': course, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def create_closedtest_view(request: HttpRequest, id, slug):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == course.author:
            if request.method == 'POST':
                body = '...'
                if 'body' in request.POST:
                    body = request.POST.get('body')

                letters = string.ascii_letters
                digits = string.digits
                all_ch = letters+digits
                pwd_length = 40
                pwd = ''.join(random.sample(all_ch, pwd_length))

                lecture = CourseYopiqTest.objects.create(lesson=lesson,course=course, slug=pwd, body=body, answer=request.POST.get('answer'))
                messages.success(request, 'Muffovviqiyatli Ma\'lumot tizimga qo\'shildi!')
                return HttpResponseRedirect(f'/courses/course/{course.id}/lesson/{lesson.slug}/closed-test/{lecture.slug}/')
            course_items = course.drag_and_drop_quizes.count() + course.lectures.count() + \
                + course.assignments.count()+course.quizess.count()+course.multi_quizess.count()
            t = 0
            for i in course.drag_and_drop_quizes.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.lectures.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.assignments.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.quizess.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.multi_quizess.all():
                if request.user in i.users.all():
                    t+=1
            answers_count = t
            foiz = 0

            if course_items!=0:
                foiz = round((answers_count/course_items)*100)
            lektures = lesson.lektures.all()
            drag_and_drops = lesson.drag_and_drop.all()
            yopiq_test = lesson.yopiq_tests.all()
            quizess = lesson.quizes.all()
            multi_quizes = lesson.multi_quizes.all()

            return render(request, 'courses/create/closed_test.html', {'lesson': lesson, 'course': course, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def create_drag_and_drop_view(request: HttpRequest, id, slug):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == course.author:
            if request.method == 'POST':
                letters = string.ascii_letters
                digits = string.digits
                all_ch = letters+digits
                pwd_length = 40
                pwd = ''.join(random.sample(all_ch, pwd_length))
                print(request.POST.get('title'))
                quiz = DragAndDropQuiz.objects.create(body=request.POST.get('title'), slug=pwd,lesson=lesson,course=course)

                for key, value in request.POST.items():
                    if key == 'csrfmiddlewaretoken' or key == 'title':
                        pass
                    else:
                        key1 = DragAndDropVariant.objects.create(quiz=quiz,body=key)
                        value = DragAndDropVariant.objects.create(quiz = quiz, body=value, key=key1)
                messages.success(request, 'Muffovviqiyatli Test tizimga qo\'shildi!')
                return JsonResponse({'slug': f'{quiz.slug}'})
            course_items = course.drag_and_drop_quizes.count() + course.lectures.count() + \
                + course.assignments.count()+course.quizess.count()+course.multi_quizess.count()
            t = 0
            for i in course.drag_and_drop_quizes.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.lectures.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.assignments.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.quizess.all():
                if request.user in i.users.all():
                    t+=1
            for i in course.multi_quizess.all():
                if request.user in i.users.all():
                    t+=1
            answers_count = t
            foiz = 0

            if course_items!=0:
                foiz = round((answers_count/course_items)*100)
            lektures = lesson.lektures.all()
            drag_and_drops = lesson.drag_and_drop.all()
            yopiq_test = lesson.yopiq_tests.all()
            quizess = lesson.quizes.all()
            multi_quizes = lesson.multi_quizes.all()

            return render(request, 'courses/create/drag_and_drop.html', {'lesson': lesson, 'course': course, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()