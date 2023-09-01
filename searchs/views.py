from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from my_messages.models import Chat
from .models import Search
from users.models import MyUser
from posts.models import Post
from django.db.models import Q
from assignments.models import Assignment, StudentAnswer

def search(request):
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
    if request.method == 'POST':
        if request.user.is_authenticated:
            posts = Post.objects.filter(
                Q(title__icontains=request.POST['body']) | Q(content__icontains=request.POST['body'])
            )
            users = MyUser.objects.filter(
                Q(username__icontains=request.POST['body'])
            )
            Search(user=request.user,body=request.POST['body']).save()
            return render(request, 'search_content.html', {'users':users, 'posts':posts, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def last_searchs(request, username):
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
        user = MyUser.objects.get(username=username)
        latest_search = Search.objects.filter(user=user).order_by('-date_searched')
        return render(request, 'users/last_search.html', {'profile':user, 'latest_search':latest_search, 'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    except MyUser.DoesNotExist:
        return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    except Search.DoesNotExist:
        return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def all_searchs_delete(request, username):
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
        user = MyUser.objects.get(username=username)
        latest_search = Search.objects.filter(user=user).order_by('-date_searched')
        for search in latest_search:
            search.delete()
        return HttpResponseRedirect(f'/users/profile/{user.username}/')
    except MyUser.DoesNotExist:
        return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})
    except Search.DoesNotExist:
        return render(request, '404.html', {'unread_assign': unread_assign, 'unread_answerca': len(unread_answerca2)})

def theme_light(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(username=request.user.username)
        user.theme = 'light'
        user.save()
        url = request.GET['url']
        return HttpResponseRedirect(url)
    else:
        return render(request, '404.html')

def theme_blue(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(username=request.user.username)
        user.theme = 'blue'
        user.save()
        url = request.GET['url']
        return HttpResponseRedirect(url)
    else:
        return render(request, '404.html')

def nav_blue(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(username=request.user.username)
        user.navbar_color = 'blue'
        user.save()
        url = request.GET['url']
        return HttpResponseRedirect(url)
    else:
        return render(request, '404.html')

def nav_brown(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(username=request.user.username)
        user.navbar_color = 'brown'
        user.save()
        url = request.GET['url']
        return HttpResponseRedirect(url)
    else:
        return render(request, '404.html')

def nav_black(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(username=request.user.username)
        user.navbar_color = 'black'
        user.save()
        url = request.GET['url']
        return HttpResponseRedirect(url)
    else:
        return render(request, '404.html')

def nav_green(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(username=request.user.username)
        user.navbar_color = 'green'
        user.save()
        url = request.GET['url']
        return HttpResponseRedirect(url)
    else:
        return render(request, '404.html')

def nav_light(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(username=request.user.username)
        user.navbar_color = 'light'
        user.save()
        url = request.GET['url']
        return HttpResponseRedirect(url)
    else:
        return render(request, '404.html')

def theme_black(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(username=request.user.username)
        user.theme = 'black'
        user.save()
        url = request.GET['url']
        return HttpResponseRedirect(url)
    else:
        return render(request, '404.html')


def theme_green(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(username=request.user.username)
        user.theme = 'green'
        user.save()
        url = request.GET['url']
        return HttpResponseRedirect(url)
    else:
        return render(request, '404.html')

def theme_brown(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(username=request.user.username)
        user.theme = 'brown'
        user.save()
        url = request.GET['url']
        return HttpResponseRedirect(url)
    else:
        return render(request, '404.html')

def edit_font(request):
    if request.user.is_authenticated:
        user = MyUser.objects.get(username=request.user.username)
        user.font = request.POST.get('font')
        user.save()
        url = request.POST['url']
        return HttpResponseRedirect(url)
    else:
        return render(request, '404.html')

def notification(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            unread_answerca = StudentAnswer.objects.filter(is_readed=False)
            unread_answerca2 = {}
            for unread_answerca1 in unread_answerca:

                if unread_answerca1.assignment.author == request.user:
                    data = {'url': f'/assignments/assignment/{unread_answerca1.assignment.id}/', 'messages': unread_answerca1.assignment.assigment_answer.filter(is_readed=False).count()}

                    unread_answerca2[f'{unread_answerca1.assignment.title}'] = data


            chats1 = Chat.objects.filter(recipient=request.user).order_by('-last_message')
            chats2 = Chat.objects.filter(author=request.user).order_by('-last_message')
            chats = chats1 | chats2
            unread_messages = {}
            for chat in chats:
                data = {}
                if request.user == chat.author:
                    if chat.messages.filter(is_read=False).exclude(user=request.user).count() != 0:
                        data['url'] = f'/chats/with/{chat.recipient.username}/'
                        data['messages'] = chat.messages.filter(is_read=False).exclude(user=request.user).count()
                        unread_messages[chat.recipient.username] = data
                else:
                    if chat.messages.filter(is_read=False).exclude(user=request.user).count() != 0:
                        data['url'] = f'/chats/with/{chat.author.username}/'
                        data['messages'] = chat.messages.filter(is_read=False).count()
                        unread_messages[chat.author.username] = data
            all = {'unread_assignments': unread_answerca2, 'unread_messages': unread_messages}
            return JsonResponse(all)
        else:
            chats1 = Chat.objects.filter(recipient=request.user).order_by('-last_message')
            chats2 = Chat.objects.filter(author=request.user).order_by('-last_message')
            chats = chats1 | chats2
            unread_messages = {}
            for chat in chats:
                data = {}
                if request.user == chat.author:
                    if chat.messages.filter(is_read=False).exclude(user=request.user).count() != 0:
                        data['url'] = f'/chats/with/{chat.recipient.username}/'
                        data['messages'] = chat.messages.filter(is_read=False).exclude(user=request.user).count()
                        unread_messages[chat.recipient.username] = data
                else:
                    if chat.messages.filter(is_read=False).exclude(user=request.user).count() != 0:
                        data['url'] = f'/chats/with/{chat.author.username}/'
                        data['messages'] = chat.messages.filter(is_read=False).count()
                        unread_messages[chat.author.username] = data

            all = {'unread_messages': unread_messages}
            return JsonResponse(all)
    else:
        return JsonResponse({'unread_messages': {}}, safe=False)


def bad_request(request, exception):
    context = {}
    return render(request, '400.html', context, status=400)


def permission_denied(request, exception):
    context = {}
    return render(request, '403.html', context, status=403)



def server_error(request):
    context = {}
    return render(request, '500.html', context, status=500)