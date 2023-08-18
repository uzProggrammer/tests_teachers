from django.core.exceptions import MultipleObjectsReturned
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.template.defaultfilters import date

from .models import Chat, Message
from django.contrib import messages
from users.models import MyUser
from django.utils import timezone

def all_chats(request):
    if request.user.is_authenticated:
        users = MyUser.objects.all()
        all_users = []
        all_users_dict = {}
        for userca in users:
            if userca != request.user:
                all_users.append(userca.username)
                d = [userca.username, userca.email]
                all_users_dict[f'{userca.username}'] = d
        try:
            chats1 = Chat.objects.filter(recipient=request.user).order_by('-last_message')
            chats2 = Chat.objects.filter(author=request.user).order_by('-last_message')
            chats = chats1 | chats2
        except Chat.DoesNotExist:
            chats = None
        return render(request, 'chats/all.html', {'chats': chats, 'all_users': all_users, 'all_users_dict': all_users_dict})
    else:
        messages.error(request, 'Siz tizimga kirmagansiz. Suhbatlarga o\'tish uchun tizimga kirish zarur')
        return HttpResponseRedirect('/users/login/')

def user_chat(request, recipient):
    if request.user.is_authenticated or request.user.username == recipient:
        chat_recipient = get_object_or_404(MyUser, username=recipient)
        try:
            try:
                chat1 = Chat.objects.get(author=request.user, recipient=chat_recipient)
                is_res = False
            except Chat.DoesNotExist:
                chat1 = Chat.objects.get(recipient=request.user, author=chat_recipient)
                is_res = True
        except:
            return render(request, '404.html')
        chats1 = Chat.objects.filter(recipient=request.user).order_by('-last_message')
        chats2 = Chat.objects.filter(author=request.user).order_by('-last_message')
        chats = chats1 | chats2
        for message in chat1.messages.all():
            if message.user != request.user:
                message.is_read = True
                message.save()
        return render(request, 'chats/chat.html', {'chat1': chat1, 'chats': chats, 'is_res': is_res,})
    else:
        return HttpResponseRedirect('/users/login/')

def get_users_for_new_chat(request):
    if request.user.is_authenticated:
        users = MyUser.objects.all()
        all_users_dict = {}
        for userca in users:
            if userca != request.user:
                d = [userca.username, userca.email]
                all_users_dict[f'{userca.username}'] = d
        return JsonResponse(all_users_dict)
    else:
        return render(request, '404.html')

def get_users_1(request):
    if request.user.is_authenticated:
        users = MyUser.objects.all()
        all_users = []
        for userca in users:
            if userca != request.user:
                all_users.append(userca.username)
        return JsonResponse(all_users)
    else:
        return render(request, '404.html')

def create_message(request, recipient):
    if request.user.is_authenticated:
        chat_recipient = MyUser.objects.get(username=recipient)


        if request.method == 'POST':
            reply = None
            if 'reply_id' in request.POST:
                reply_id = request.POST['reply_id']
                try:
                    reply = Message.objects.get(id=int(reply_id))
                except Message.DoesNotExist:
                    reply = None
            message = request.POST['message']
            chat_id = request.POST['chat_id']
            try:
                chat = Chat.objects.get(id=int(chat_id))
            except Chat.DoesNotExist:
                chat = None
            user = request.user
            if reply:
                if 'is_recipient' in request.POST:
                    Message(user=user,message=message,parent=reply, is_recipient=True).save()
                else:
                    Message(user=user, message=message,  parent=reply).save()
            else:
                if 'is_recipient' in request.POST:
                    Message(user=user, message=message, is_recipient=True).save()
                else:
                    Message(user=user, message=message,).save()
            last = Message.objects.last()
            chat = Chat.objects.get(id=chat_id)
            chat.last_message = timezone.now()
            chat.last_message_text = last
            chat.messages.add(last)
            chat.save()
            data = {f'message-{last.id}': last.message, 'date_created': date(last.date_created, 'd.m.Y | H:i'), 'author': user.username, 'is_readed': last.is_read}
            data['id'] = f'{last.id}'

            return JsonResponse(data)
    else:
        return HttpResponseRedirect('users/login/')

def get_unread_message(request, recipient):
    if request.user.is_authenticated:
        chat_recipient = get_object_or_404(MyUser, username=recipient)
        try:
            chat = Chat.objects.get(author=request.user, recipient=chat_recipient)
        except:
            chat = Chat.objects.get(recipient=request.user, author=chat_recipient)
        messages = chat.messages.filter(is_read=False)
        if messages == '':
            return HttpResponse('')
        else:
            import random
            data = {}
            for message in messages:
                if request.user == message.user:
                    pass
                else:
                    data2 = {}
                    data2[f'user'] = message.user.username
                    data2[f'message'] = message.message
                    data2[f'date_send'] = date(message.date_created, 'd.m.Y | H:i')
                    data[f'{message.id}'] = data2

            return JsonResponse(data)
    else:
        return HttpResponseRedirect('/users/login/')

def delete_message(request, recipient):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                message_id = int(request.POST['message_id'])
            except:
                return render(request, '404.html')
            a = Message.objects.get(id=message_id)
            a.delete()
            return JsonResponse({'status':'ok'})
        else:
            return render(request, '404.html')
    else:
        return HttpResponseRedirect('/users/login/')

def update_message(request, recipient):
    if request.user.is_authenticated:
        if request.method=='POST':
            id = int(request.POST['message_id'])
            message = request.POST['message']
            m = Message.objects.get(id=id)
            m.update(message=message)
            return JsonResponse(
                {'message': m.message}
            )
        else:
            return render(request, '404.html')
    else:
        return HttpResponseRedirect('users/login/')

def change_notification(request, recipient):
    if request.user.is_authenticated:
        if request.method == 'POST':
            chat_id = int(request.POST['chat_id'])
            chat = Chat.objects.get(id=chat_id)
            if 'onn_res' in request.POST:
                chat.recipient_notification = True
            elif 'off_res' in request.POST:
                chat.recipient_notification = False
            elif 'on_aut' in request.POST:
                chat.author_notification = True
            else:
                chat.author_notification = False
            chat.save()
            return JsonResponse({'status': 'ok'})
        else:
            return render(request, '404.html')
    else:
        return HttpResponseRedirect('users/login/')

def create_chat(request, recipient):
    if request.user.is_authenticated:
        recipient = get_object_or_404(MyUser, username=recipient)
        chats1 = Chat.objects.filter(author=request.user, recipient=recipient)
        chats2 = Chat.objects.filter(author=recipient, recipient=request.user)

        chats = chats1 & chats2
        if len(chats) == 0:
            chat = Chat.objects.create(author=request.user, recipient=recipient)
            return HttpResponseRedirect(f'/chats/with/{chat.recipient.username}/')
        else:
            return HttpResponseRedirect(f'/chats/with/{recipient}/')
    else:
        return HttpResponseRedirect('users/login/')