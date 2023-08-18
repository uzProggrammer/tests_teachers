from django.utils.timezone import now
from .models import MyUser


class SetLastVisitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            user = MyUser.objects.get(id=request.user.id)
            user.last_visit=now()
            user.save()
        return response