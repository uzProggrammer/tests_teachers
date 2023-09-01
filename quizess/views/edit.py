from django.shortcuts import render, get_object_or_404
from quizess.models import Quiz
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib import messages

def edit_quiz_view(request: HttpRequest, id):
    test = get_object_or_404(Quiz, id=id)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user == test.author:
            if request.method == 'POST':
                title = request.POST.get('title')
                test.title = title

                body = 'Test'
                if 'body' in request.POST:
                    body = request.POST.get('body')
                test.summary = body

                diff = request.POST.get('diff')
                test.type = diff

                time = request.POST.get('time') if 'time' in request.POST else '00:10'
                test.time = time
                test.save()
                messages.success(request, f'Muvvofiqiyatli {test.title} tahrirlandi!')
                return HttpResponseRedirect(f'/tests/test/{id}/')
            return render(request, 'tests/edit.html', context={'test':test})
        else:
            return render(request, '403.html', status=403)
    else:
        return render(request, '403.html', status=403)