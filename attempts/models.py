from django.db import models
from problems.models import Problem
from users.models import MyUser

class Attempt(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='problem_attempt')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_attempt')
    time = models.FloatField()
    memory = models.FloatField()
    holat = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    code = models.TextField()
    def __str__(self):
        return f'{self.author} attempt {self.problem}'