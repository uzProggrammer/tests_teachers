from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
import json
from users.models import MyUser

@csrf_exempt
def login_api(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        try:
            user = MyUser.objects.get(username=username)
        except:
            return JsonResponse({'status': 'User not found'})
        
        if user.check_password(password):
            return JsonResponse({'status': 'ok', 'api_token': user.api_token, 'username':user.username, 'full_name': user.get_full_name()})
        else:
            return JsonResponse({'status': 'Password not true'})
    else:
        return JsonResponse({'status': 'error'})
    
def notification(request, ):
    pass