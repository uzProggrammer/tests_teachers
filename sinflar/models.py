from django.db import models

from users.models import MyUser


class Sinf(models.Model):
    nom = models.CharField(max_length=4)
    students = models.ManyToManyField(MyUser, related_name='class_students', null=True, blank=True)
    url = models.SlugField()
    author_student = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='class_author', null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    max_students = models.IntegerField(default=24)
    ball = models.FloatField(default=0.0)
    active_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='class_active_user', null=True, blank=True)


    def __str__(self):
        return self.nom