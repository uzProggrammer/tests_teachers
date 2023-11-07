import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from my_messages.models import Chat, Message
from users.models import MyUser
from apiv1.naturaltime import naturaltime
from django.db.models import Q


@csrf_exempt
def all_chats(request, auth_token):
    try:
        user = MyUser.objects.get(api_token=auth_token)
        try:
            chats1 = Chat.objects.filter(recipient=user).order_by('-last_message')
            chats2 = Chat.objects.filter(author=user).order_by('-last_message')
            chats = chats1 | chats2
        except:
            chats = []
        chats1 = [
            {
                'name': chat.recipient.get_full_name()[:15]+'...' if user==chat.author else chat.author.get_full_name()[:15]+"...",
                'email': chat.get_custom_last_m()[:20] if len(chat.get_custom_last_m())!=0 else chat.recipient.username if user==chat.author else chat.author.username,
                'status': user.get_last_visit(),
                'id': chat.id,
                'new-m': chat.messages.filter(is_read=False).exclude(user=user).count()
            } for chat in chats
        ]
        return JsonResponse(chats1, safe=False)
    except MyUser.DoesNotExist:
        return JsonResponse({'status': 'This user is not defined'})

@csrf_exempt
def user_chat(request, auth_token, id1):
    try:
        user = MyUser.objects.get(api_token=auth_token)
        try:
            chat = Chat.objects.get(id=id1)
            all_messages = [
                {
                    'message': me.message,
                    'is_recipient': me.is_recipient,
                    'readed': me.is_read,
                    'id': me.id,
                    'date': naturaltime(me.date_created)
                } for me in chat.messages.all()
            ]
            return JsonResponse(all_messages, safe=False)
        except:
            return JsonResponse([], safe=False)
        
    except MyUser.DoesNotExist:
        return JsonResponse({'status': 'This user is not defined'})

@csrf_exempt
def get_search_users(request, auth_token):
    try:
        search = request.GET.get('q')
        user=MyUser.objects.get(api_token=auth_token)
        users = MyUser.objects.exclude(id=user.id).filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
        users_list = [
            {
                'name': user.get_full_name(),
                'status': user.get_last_visit(),
                'username': user.username,
                'id': user.id,
            } for user in users
        ]
        return JsonResponse(users_list, safe=False)
    except MyUser.DoesNotExist:
        return JsonResponse({'status': 'This user is not defined'})

@csrf_exempt
def start_chat(request, auth_token,res_id):
    try:
        user=MyUser.objects.get(api_token=auth_token)
        res=MyUser.objects.get(id=res_id)
        chat1=Chat.objects.filter(author=user, recipient=res)
        chat2=Chat.objects.filter(recipient=user, author=user)
        chat = chat1 | chat2
        if len(chat)==0:
            chat=Chat.objects.create(author=user, recipient=res, )
            chat = {
                'name': chat.recipient.get_full_name() if user==chat.author else chat.author.get_full_name(),
                'email': chat.recipient.username,
                'status': user.get_last_visit(),
                'id': chat.id,
            }
        else:
            chat=chat[0]
            chat = {
                'name': chat.recipient.get_full_name() if user==chat.author else chat.author.get_full_name(),
                'email': chat.recipient.username,
                'status': user.get_last_visit(),
                'id': chat.id,
            }
        return JsonResponse(chat, safe=False)
    except MyUser.DoesNotExist:
        return JsonResponse({'status': 'This user is not defined'})

@csrf_exempt
def create_message(reqeust, auth_token, id):
    try:
        user=MyUser.objects.get(api_token=auth_token)
        chat = Chat.objects.get(id=id)
        if reqeust.method=='POST':
            data = json.loads(reqeust.body)
            message = data.get('message')
            if chat.author == user:
                is_res = False
            elif chat.recipient==user:
                is_res = True
            else:
                return JsonResponse({'status': f'You have not this chat'})
            message1 = Message.objects.create(message=message,user=user, is_recipient=is_res)
            chat.messages.add(message1)
            chat.last_message=message1.date_created
            chat.last_message_text=message1
            chat.save()
            all_messages = [
                {
                    'message': me.message,
                    'is_recipient': me.is_recipient,
                    'readed': me.is_read,
                    'id': me.id,
                    'date': naturaltime(me.date_created)
                } for me in chat.messages.all()
            ]
            return JsonResponse(all_messages, safe=False)
        else:
            return JsonResponse({'status': f'[{reqeust.method}] method is not allowed'})
    except:
        return JsonResponse({'status': 'This user is not defined'})

@csrf_exempt
def delete_message(reqeust, auth_token, id, id1):
    try:
        user=MyUser.objects.get(api_token=auth_token)
        chat = Chat.objects.get(id=id)
        if chat.author == user:
            is_res = False
        elif chat.recipient==user:
            is_res = True
        else:
            return JsonResponse({'status': 'You have not this chat'})
        try:
            message=Message.objects.get(id=id1)
            chat.messages.remove(message)
            return JsonResponse({'status': 'Ok'})
        except Message.DoesNotExist:
            return JsonResponse({'status': 'This message is not exists'})
    except MyUser.DoesNotExist and Chat.DoesNotExist:
        return JsonResponse({'status': 'This user or chat is not defined'})

def delete_chat(request, auth_token, id):
    try:
        user=MyUser.objects.get(api_token=auth_token)
        chat = Chat.objects.get(id=id,)
        if chat.author == user:
            is_res = False
        elif chat.recipient==user:
            is_res = True
        else:
            return JsonResponse({'status': f'You have not this chat'})
        chat.delete()
        return JsonResponse({'status':'ok'})
    except MyUser.DoesNotExist or Chat.DoesNotExist:
        return JsonResponse({'status': 'This user or chat is not defined'})