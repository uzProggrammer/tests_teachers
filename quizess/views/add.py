from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect
from quizess.models import Quiz, DefoultQuiz, DefoultQuizVariant, DragAndDrop, DragAndDropVariants, DefaultQuizAnswer, DefoulMultitQuiz, DefoulMultitQuizAnswer, DefoulMultitQuizVariant, DragAndDropAnswer, ClosedTest
from django.contrib import messages

def add_quiz(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_teacher or request.user.is_create_test:
            if request.method == 'POST':
                title = request.POST.get('title')
                body = 'Test'
                if 'body' in request.POST:
                    body = request.POST.get('body')
                diff = request.POST.get('diff')
                time = request.POST.get('time') if 'time' in request.POST else '00:10'
                test = Quiz.objects.create(title=title,summary=body, type=diff, time=time, author=request.user)
                messages.success(request, 'Test muvaffaqiyatli tizimga qo\'shildi')
                return HttpResponseRedirect(f'/tests/test/{test.id}/')
            return render(request, 'tests/add.html', )
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '403.html', status=403)

def add_test_view(request: HttpRequest, id):
    test =  get_object_or_404(Quiz, id=id)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_teacher or request.user.is_create_test:
            if request.method == 'POST':
                quiz_type = request.POST.get('quiz-type')
                if quiz_type == 'quiz':
                    quiz_title = request.POST.get('quiz-1-title')
                    ball = request.POST.get('ball') if 'ball' in request.POST else 2.0
                    quiz1 = DefoultQuiz.objects.create(quiz=test, body=quiz_title,author=request.user, ball=ball)
                    test.quizes_count += 1
                    test.save(update_fields=['quizes_count'])
                    for key,value in request.POST.items():
                        if key!='csrfmiddlewaretoken' and key!='quiz-type' and key!='quiz-1-title' and key!='is-true-1' and key!='ball':
                            key = key.split()[-1]
                            is_true = request.POST.get('is-true-1')
                            if int(key.split('-')[-1]) == int(is_true):
                                DefoultQuizVariant.objects.create(default_quiz=quiz1,is_true=True,body=value)
                            else:
                                DefoultQuizVariant.objects.create(default_quiz=quiz1, body=value)


                elif quiz_type == 'multi-quiz':
                    quiz_title = request.POST.get('quiz-1-title')
                    ball = request.POST.get('ball') if 'ball' in request.POST else 2.0
                    quiz1 = DefoulMultitQuiz.objects.create(quiz=test, body=quiz_title,author=request.user, ball=ball)
                    test.quizes_count += 1
                    test.save(update_fields=['quizes_count'])
                    for key,value in request.POST.items():
                        if key!='csrfmiddlewaretoken' and key!='quiz-type' and key!='quiz-1-title' and key!='is-true-1' and key!='ball':
                            key = key.split()[-1]
                            is_true = request.POST.getlist('is-true-1')
                            if key.split('-')[-1] in is_true:
                                DefoulMultitQuizVariant.objects.create(default_quiz=quiz1,is_true=True,body=value)
                            else:
                                DefoulMultitQuizVariant.objects.create(default_quiz=quiz1, body=value)


                elif quiz_type == 'drag-and-drop':
                    ball = request.POST.get('ball') if 'ball' in request.POST else 2.0
                    dr = DragAndDrop.objects.create(quiz=test, body=request.POST.get('title'), ball=ball)
                    test.quizes_count += 1
                    test.save(update_fields=['quizes_count'])
                    for i in request.POST.keys():
                        if i!='csrfmiddlewaretoken' and i!='quiz-type' and i!='title':
                            key1 = DragAndDropVariants.objects.create(quiz_dr=dr, body=i)
                            value = DragAndDropVariants.objects.create(quiz_dr=dr, parent=key1, body=request.POST.get(i))

                elif quiz_type == 'closed-test':
                    ball = request.POST.get('ball') if 'ball' in request.POST else 0.0
                    body = request.POST.get('body') if 'body' in request.POST else '...'
                    true_answer = request.POST.get('true_answer') if 'true_answer' in request.POST else '.'
                    cl = ClosedTest.objects.create(ball=ball, body=body, author=request.user, quiz=test, true_answer=true_answer)
                    test.quizes_count+=1
                    test.save()
                messages.success(request, 'Savol muvvofiqiyatli yaratildi!')
                return HttpResponseRedirect(f'/tests/test/{id}/')
            return render(request, 'tests/add_quiz.html', {'test': test})
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '403.html', status=403)