from django.shortcuts import render, get_object_or_404
from .models import Attempt
from django.core.paginator import Paginator
from assignments.models import Assignment, StudentAnswer

def all_attempts(request):
    attempts = Attempt.objects.all().order_by('-id')
    object = Paginator(attempts, 40)

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
    return render(request, 'attempts/all.html', {'object_list':object, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def attempt_detail(request, id):
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
    attempt = get_object_or_404(Attempt, id=id)
    return render(request, 'attempts/attempt.html', {'attempt': attempt, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})