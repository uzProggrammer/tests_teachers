import json
from tracemalloc import is_tracing
from django.shortcuts import render, get_object_or_404
from .models import Course, CourseMultiQuiz, CourseQuiz, CourseQuizVariant, CourseYopiqTest, DragAndDropAnswer, DragAndDropQuiz, DragAndDropVariant, Lectures, Lessons, MultiQuizAnswer, MultiQuizVariuant, QuizAnswer, YopiqTestAnswer
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse, HttpRequest
from django.contrib import messages

print(1)
def all_lessons_view(request):
    courses = Course.objects.all()
    return render(request, 'courses/all.html', {'courses': courses})


def get_course_view(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'courses/course.html', {'course': course})

def start_course_view(request, course_id):
    if request.user.is_authenticated:
        course = get_object_or_404(Course, id=course_id)
        if request.user in course.users.all():
            return HttpResponseRedirect(f'/courses/course/{course_id}/')
        else:
            course.users.add(request.user)
            messages.success(request, 'Siz Kursga movofiqiyatli obuna bo\'ldingiz')
            return HttpResponseRedirect(f'/courses/course/{course_id}/')
    else:
        return HttpResponseForbidden()

def lesson_view(request, id, slug):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug, course=course)
    if request.user.is_authenticated:
        if request.user in course.users.all():
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
            return render(request, 'courses/lesson.html', {'is_lesson': True, 'course': course, 'lesson': lesson, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def get_lessens_view(request, id):
    course = get_object_or_404(Course, id=id)
    if request.user.is_authenticated:
        if request.user in course.users.all():
            data = {}
            for el in course.lessons.all():
                data1 = []
                lesson_items = el.drag_and_drop.count() + el.lektures.count() + \
                                        + el.yopiq_tests.count()+el.quizes.count()+el.multi_quizes.count()
                t = 0
                for i in el.drag_and_drop.all():
                    if request.user in i.users.all():
                        t+=1
                for i in el.yopiq_tests.all():
                    if request.user in i.users.all():
                        t+=1
                for i in el.quizes.all():
                    if request.user in i.users.all():
                        t+=1
                for i in el.lektures.all():
                    if request.user in i.users.all():
                        t+=1
                for i in el.multi_quizes.all():
                    if request.user in i.users.all():
                        t+=1
                answers_count = t
                
                foiz = 0
                if lesson_items!=0:
                    foiz = round((answers_count/lesson_items)*100)
                answers_count = t
                data1.append(foiz)
                data1.append(el.slug)
                data1.append(el.summary)
                data[el.title] = data1
            return JsonResponse(data)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def lecture_view(request, id, slug, slug1):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug, course=course)
    lecture = get_object_or_404(Lectures, slug=slug1)
    if request.user.is_authenticated:
        if request.user in course.users.all():
            lecture.users.add(request.user)
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
            return render(request, 'courses/lesson.html', {'lecture': lecture,  'course': course, 'lesson': lesson, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def quiz_view(request,id, slug, slug1):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug, course=course)
    quiz = get_object_or_404(CourseQuiz, slug=slug1)
    if request.user.is_authenticated:
        if request.user in course.users.all():
            if request.method == 'POST':
                value = int(request.POST.get('variant-quiz'))
                variant = get_object_or_404(CourseQuizVariant, id=value)
                if variant.is_true:
                    answer = QuizAnswer.objects.filter(quiz=quiz, course=course, user=request.user, lesson=lesson, is_true=True)
                    if answer.count() == 0:
                        QuizAnswer.objects.create(quiz=quiz, course=course, user=request.user, lesson=lesson, variant=variant, is_true=True)
                    quiz.users.add(request.user)
                    messages.success(request, 'Javobingiz to\'g\'ri!')
                    return HttpResponseRedirect(f'/courses/course/{id}/lesson/{slug}/quiz/{slug1}/')
                else:
                    answer = QuizAnswer.objects.filter(quiz=quiz, course=course, user=request.user, lesson=lesson, is_true=False)
                    if answer.count() == 0:
                        QuizAnswer.objects.create(quiz=quiz, course=course, user=request.user, lesson=lesson, variant=variant, is_true=False)
                    messages.error(request, 'Javobingiz nato\'g\'ri!')
                    return HttpResponseRedirect(f'/courses/course/{id}/lesson/{slug}/quiz/{slug1}/')
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
            answer = QuizAnswer.objects.filter(quiz=quiz, course=course, user=request.user, lesson=lesson).order_by('-is_true')
            if answer.count() > 0:
                answer = answer[0]
            else:
                answer = None
            return render(request, 'courses/lesson.html', {'answer':answer, 'quiz':quiz,'course': course, 'lesson': lesson, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def closed_quiz_view(request,id, slug, slug1):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug, course=course)
    quiz = get_object_or_404(CourseYopiqTest, slug=slug1)
    if request.user.is_authenticated:
        if request.user in course.users.all():
            if request.method == 'POST':
                value = request.POST.get('closed-test-body')
                if value == quiz.answer:
                    quiz.users.add(request.user)
                    YopiqTestAnswer.objects.create(test=quiz, course=course, user=request.user, lesson=lesson, is_true=True, answer=value)
                    messages.success(request, 'Javobingiz to\'g\'ri!')
                else:
                    YopiqTestAnswer.objects.create(test=quiz, course=course, user=request.user, lesson=lesson, answer=value, is_true=False)
                    messages.error(request, 'Javobingiz nato\'g\'ri!')
                return HttpResponseRedirect(f'/courses/course/{id}/lesson/{slug}/closed-test/{slug1}/')

                
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
            answer = YopiqTestAnswer.objects.filter(test=quiz, course=course, user=request.user, lesson=lesson).order_by('-is_true', '-id')
            if answer.count() > 0:
                answer = answer[0]
            else:
                answer = None
            return render(request, 'courses/lesson.html', {'answer_yopiq':answer, 'quiz_yopiq':quiz,'course': course, 'lesson': lesson, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def drag_and_drop(request,id, slug, slug1):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug, course=course)
    quiz = get_object_or_404(DragAndDropQuiz, slug=slug1)
    if request.user.is_authenticated:
        if request.user in course.users.all():
            if request.method == 'POST':
                pass
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
            answer = DragAndDropAnswer.objects.filter(test=quiz, course=course, user=request.user, lesson=lesson).order_by('-is_true')
            quizes1 = {}
            if answer.count() > 0:
                answer = answer[0]
                answers = answer.answer.split('    ')
                for answer in answers:
                    answer = answer.split('-')
                    if len(answer)>1:
                        quizes1[DragAndDropVariant.objects.get(id=int(answer[0]))] = DragAndDropVariant.objects.get(id=int(answer[1]))

            else:
                answer = None
            return render(request, 'courses/lesson.html', {'quizes1':quizes1, 'answer_drag_and_drop':answer, 'drag_and_drop':quiz,'course': course, 'lesson': lesson, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()

def drag_and_drop_post(request: HttpRequest,id, slug, slug1):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug, course=course)
    quiz = get_object_or_404(DragAndDropQuiz, slug=slug1)
    if request.user.is_authenticated:
        if request.user in course.users.all():
            if request.method == 'POST':
                data = {}
                for key in request.POST.keys():
                    if key != 'csrfmiddlewaretoken':
                        for value in request.POST.getlist(key):
                            key1 = int(key[:len(key)-2])
                            variant = DragAndDropVariant.objects.get(id=key1)
                            variant1 = DragAndDropVariant.objects.get(id=value)
                            if variant1.key == variant:
                                pass
                            else:
                                data['error'] = True
                                break
                post_data = json.dumps(request.POST)
                post_data = json.loads(post_data)
                post_data.pop('csrfmiddlewaretoken', None)
                if 'error' in data:
                    data = ''
                    for key, value in post_data.items():
                        data += f'{str(key)[:len(key)-2]} - {value}    '
                    answer = DragAndDropAnswer.objects.create(user=request.user, test=quiz, is_true=False, answer=data, lesson=lesson, course=course)
                    messages.error(request, 'Javobingiz nato\'g\'ri qaytadan urinib ko\'ring')
                    return JsonResponse({'status': 'error'})
                else:
                    data = ''
                    for key, value in post_data.items():
                        data += f'{str(key)[:len(key)-2]} - {value}    '
                    answer = DragAndDropAnswer.objects.create(user=request.user, test=quiz, is_true=False, answer=data, lesson=lesson, course=course)
                    quiz.users.add(request.user)
                    messages.success(request, 'Javobingiz to\'g\'ri')
                    return JsonResponse({'status': 'success'})
            else:
                JsonResponse({'error': 'Method GET not allowed'})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()


def get_multi_quiz_view(request: HttpRequest,id, slug, slug1):
    course = get_object_or_404(Course, id=id)
    lesson = get_object_or_404(Lessons, slug=slug, course=course)
    quiz = get_object_or_404(CourseMultiQuiz, slug=slug1)
    if request.user.is_authenticated:
        if request.user in course.users.all():
            if request.method == 'POST':
                variants = request.POST.getlist('variant')
                data = []
                for i in variants:
                    variant = MultiQuizVariuant.objects.get(id=int(i))
                    if variant.is_true == False:
                        data.append('error')
                
                if 'error' in data:
                    answer = MultiQuizAnswer.objects.create(user=request.user, quiz=quiz, is_true=False, lesson=lesson, course=course)
                    for i in variants:
                        variant = MultiQuizVariuant.objects.get(id=int(i))
                        answer.variants.add(variant)
                        answer.save()
                    messages.error(request,'Javobingiz nato\'g\'ri qaytadan urinib ko\'ring')
                    return HttpResponseRedirect(f'/courses/course/{id}/lesson/{slug}/multi-quiz/{slug1}/')
                else:
                    answer = MultiQuizAnswer.objects.create(user=request.user, quiz=quiz, is_true=True, lesson=lesson, course=course)
                    for i in variants:
                        variant = MultiQuizVariuant.objects.get(id=int(i))
                        answer.variants.add(variant)
                        answer.save()
                    quiz.users.add(request.user)
                    messages.success(request, 'Javobingiz to\'g\'ri!')
                    return HttpResponseRedirect(f'/courses/course/{id}/lesson/{slug}/multi-quiz/{slug1}/')

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
            answer = MultiQuizAnswer.objects.filter(quiz=quiz, course=course, user=request.user, lesson=lesson).order_by('-is_true', '-id')
            if answer.count() > 0:
                answer = answer[0]
            else:
                answer = None
            return render(request, 'courses/lesson.html', {'multi_answer':answer, 'multi_quiz':quiz,'course': course, 'lesson': lesson, 'course_items':course_items, 'answers_count': answers_count,'foiz':foiz, 'lektures': lektures,'drag_and_drops':drag_and_drops, 'yopiq_test':yopiq_test, 'quizess': quizess, 'multi_quizes': multi_quizes})
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseForbidden()