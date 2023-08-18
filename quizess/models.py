from django.db import models
from users.models import MyUser
from ckeditor.fields import RichTextField

class Task(models.Model):
    author = models.ForeignKey(MyUser, related_name='author_test', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    about = RichTextField()
    actioned_users = models.ManyToManyField(MyUser, related_name='actioned_users', blank=True, null=True)
    users = models.ManyToManyField(MyUser, blank=True, related_name='tasks', null=True)
    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    ball = models.FloatField(default=4)

    def __str__(self):
        return self.title

class TaskQuestion(models.Model):
    q_id=models.IntegerField(default=0)
    task = models.ForeignKey(Task, related_name='answer', on_delete=models.CASCADE)
    body = RichTextField()
    def __str__(self):
        return self.body

class QuestionAnswers(models.Model):
    question = models.ForeignKey(TaskQuestion, on_delete=models.CASCADE, related_name='answer')
    body = models.TextField()
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.body

class Result(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_result')
    test = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='test_result')
    scope = models.FloatField()

    def __str__(self):
        return str(self.pk)