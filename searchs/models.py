from django.db import models
from users.models import MyUser


class Search(models.Model):
    user = models.ForeignKey(MyUser, related_name='search_user', on_delete=models.CASCADE)
    body = models.CharField(max_length=1000)
    date_searched = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body