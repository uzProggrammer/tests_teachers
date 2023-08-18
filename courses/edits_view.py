import json

from tracemalloc import is_tracing
from django.shortcuts import render, get_object_or_404
from .models import Course, CourseMultiQuiz, CourseQuiz, CourseQuizVariant, CourseTag, CourseYopiqTest, DragAndDropAnswer, DragAndDropQuiz, DragAndDropVariant, Lectures, Lessons, MultiQuizAnswer, MultiQuizVariuant, QuizAnswer, YopiqTestAnswer
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse, HttpRequest
from django.contrib import messages
import random, string


def edit_course_view(request: HttpRequest, id):
    course = get_object_or_404(Course, id=id)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_teacher:
            if request.method == 'POST':
                body = '...'
                if 'body' in request.POST:
                    body = request.POST.get('body', None)
                course.author = request.user
                course.title = request.POST.get('title', None)
                course.summary = request.POST.get('summary', None)
                course.about = body
                course.save()
                if 'teg' in request.POST:
                    for i in request.POST.getlist('teg'):
                        teg = CourseTag.objects.get_or_create(title=i)
                        course.tags.add(teg[0])
                        course.save()
                messages.success(request, 'Muffiqiyatli Kurs tahrirlandi! ')
                return HttpResponseRedirect(f'/courses/course/{course.id}/')
            return render(request, 'courses/edit/course.html', {'course': course})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def edit_lesson_view(request: HttpRequest, id, slug):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == course.author:
            body = '...'
            if 'body' in request.POST:
                body = request.POST.get('body')
            

            title = request.POST.get('title')
            lesson.title = title
            lesson.summary = body
            lesson.course = course
            lesson.save()
            messages.success(request, 'Dars Kursga muffiqiyatli tahrirlandi')
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

def edit_lecture_view(request, id, slug, slug1):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug, course=course)
    lecture = get_object_or_404(Lectures, slug=slug1)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == course.author:
            if request.method == 'POST':
                lecture.body = request.POST.get('body')
                lecture.save()
                messages.success(request, 'Mufofiqiyatli tahrirlandi')
                return HttpResponseRedirect(f'/courses/course/{id}/lesson/{slug}/lecture/{slug1}')
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
            return render(request, 'courses/edit/lesson.html', {'lecture': lecture,  'course': course, 'lesson': lesson, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def edit_drag_and_drop_view(request: HttpRequest, id, slug, slug1):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug)
    quiz = get_object_or_404(DragAndDropQuiz, slug=slug1)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == course.author:
            if request.method == 'POST':
                variants = quiz.variants.all()
                for variant in variants:
                    variant.delete()
                quiz.body = request.POST.get('title')
                for key, value in request.POST.items():
                    if key == 'csrfmiddlewaretoken' or key == 'title':
                        pass
                    else:
                        key1 = DragAndDropVariant.objects.create(quiz=quiz, body=key)
                        value = DragAndDropVariant.objects.create(quiz = quiz, body=value, key=key1)

                messages.success(request, 'Muffovviqiyatli Test tahrirlandi')
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

            return render(request, 'courses/edit/drag_and_drop.html', { 'drag_and_drop':quiz,'lesson': lesson, 'course': course, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def edit_closedtest_view(request: HttpRequest, id, slug, slug1):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug)
    quiz = get_object_or_404(CourseYopiqTest, slug=slug1)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == course.author:
            if request.method == 'POST':
                body = '...'
                if 'body' in request.POST:
                    body = request.POST.get('body')
                quiz.body=body
                quiz.answer=request.POST.get('answer')
                messages.success(request, 'Muffovviqiyatli Test tahrirlandi')
                return HttpResponseRedirect(f'/courses/course/{course.id}/lesson/{lesson.slug}/closed-test/{quiz.slug}/')
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

            return render(request, 'courses/edit/closed_test.html', {'quiz':quiz, 'lesson': lesson, 'course': course, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def edit_multiquiz_view(request: HttpRequest, id, slug, slug1):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug)
    quiz = get_object_or_404(CourseMultiQuiz, slug=slug1)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == course.author:
            if request.method == 'POST':
                quiz1 = request.POST
                quiz.body=request.POST['quiz-title']
                quiz.save()
                new_answer = quiz
                variants = new_answer.variants.all()
                for variant in variants:
                    variant.delete()
                is_true = request.POST.getlist('is_true')
                for answer_key, answer_value in quiz1.items():
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

            return render(request, 'courses/edit/multiquiz.html', {'quiz':quiz, 'lesson': lesson, 'course': course, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def edit_quiz_view(request: HttpRequest, id, slug, slug1):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug)
    quiz = get_object_or_404(CourseQuiz, slug=slug1)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == course.author:
            if request.method == 'POST':
                quiz1 = request.POST
                quiz.body=request.POST['quiz-title']
                new_answer = quiz
                is_true = int(request.POST['is_true'])
                variants = quiz.variants.all()
                for variant in variants:
                    variant.delete()
                for answer_key, answer_value in quiz1.items():
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

            return render(request, 'courses/edit/quiz.html', {'quiz':quiz, 'lesson': lesson, 'course': course, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()