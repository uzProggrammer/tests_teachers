from django.db import models
from users.models import  MyUser
from ckeditor.fields import  RichTextField

class Problem(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_task')
    title = models.CharField(max_length=150)
    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=16)
    difficulty = models.IntegerField(default=1)
    about = RichTextField()
    info_out = models.TextField(blank=True, null=True)
    info_in = models.TextField(blank=True, null=True)
    simple_tests = models.JSONField(null=True,blank=True)
    tests = models.JSONField()
    yechim = models.TextField(blank=True, null=True,)
    date_created = models.DateTimeField(auto_now_add=True)
    accepteds = models.ManyToManyField(MyUser, related_name='user_problem_accepted', null=True, blank=True)
    foiz = models.FloatField(default=0)
    wrong_answers = models.ManyToManyField(MyUser, related_name='user_problem_wrong_answers', null=True, blank=True)

    def __str__(self):
        return self.title

class TaskComment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='problem_comment_user')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='problem_comment')
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} comment on {self.problem}'
