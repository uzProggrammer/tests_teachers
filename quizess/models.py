import re
from django.db import models
from users.models import MyUser
from django.contrib.humanize.templatetags.humanize import naturaltime
import bs4

class Quiz(models.Model):
    title = models.CharField(max_length=10000)
    users = models.ManyToManyField(MyUser, related_name='tasks')
    time = models.TimeField()
    author = models.ForeignKey(MyUser,  on_delete=models.CASCADE, related_name='author_test')
    summary = models.TextField()
    types = (
        ('Oson', 'Oson'),
        ('O\'rtacha', 'O\'rtacha'),
        ('Qiyin', 'Qiyin'),
        ('Juda Qiyin', 'Juda Qiyin'),
    )
    type = models.CharField(max_length=100, choices=types)
    is_public = models.BooleanField(default=False)
    quizes_count = models.IntegerField(default=0)

    not_actioned_users = models.ManyToManyField(MyUser, related_name='tasks_not_actioned')

    def __str__(self) -> str:
        return self.title.title()

    def get_custom_body(self):
        return bs4.BeautifulSoup(self.summary, 'html.parser').get_text()
    
    



class DragAndDrop(models.Model):
    body = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='drag_and_drop')
    actiened_users = models.ManyToManyField(MyUser, null=True, blank=True, related_name='drag_and_drop_quizess')
    date_created = models.DateTimeField(auto_now=True)

    ball = models.FloatField(default=0.0)
    def get_keys(self):
        keys = self.variants.all().order_by('?')
        d = []
        for i in keys:
            if not i.parent:
                d.append(i)
        return d
    
    def get_values(self):
        keys = self.variants.all().order_by('?')
        d = []
        for i in keys:
            if not i.parent:
                pass
            else:
                d.append(i)
        return d

class DragAndDropVariants(models.Model):
    quiz_dr = models.ForeignKey(DragAndDrop, on_delete=models.CASCADE, related_name='variants')
    body = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child', null=True, blank=True)

class DragAndDropAnswer(models.Model):
    actioned_user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='dad_answer')
    test = models.ForeignKey(DragAndDrop, on_delete=models.CASCADE, related_name='answer')
    is_true = models.BooleanField(default=False)
    answer = models.CharField(max_length=99999999999999)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='drag_and_drop_answers')



class DefoultQuiz(models.Model):
    body = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='my_quizes')
    users = models.ManyToManyField(MyUser, related_name='accepted_quizess', null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='default_quizes')

    date_created = models.DateTimeField(auto_now=True)
    ball = models.FloatField(default=0.0)
    def get_variants(self):
        return self.variants.order_by('?')

    
class DefoultQuizVariant(models.Model):
    default_quiz = models.ForeignKey(DefoultQuiz, on_delete=models.CASCADE,related_name='variants')
    is_true = models.BooleanField(default=False)
    body = models.TextField()

class DefaultQuizAnswer(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='my_answer_default_quiz')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='default_quiz_answers')
    is_true = models.BooleanField(default=False)
    default_quiz = models.ForeignKey(DefoultQuiz, on_delete=models.CASCADE,related_name='answers')



class DefoulMultitQuiz(models.Model):
    body = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='my_multi_quizes')
    users = models.ManyToManyField(MyUser, related_name='accepted_multi_quizess', null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='default_multi_quizes')
    ball = models.FloatField(default=0.0)
    date_created = models.DateTimeField(auto_now=True)
    def get_variants(self):
        return self.variants.order_by('?')
    
class DefoulMultitQuizVariant(models.Model):
    default_quiz = models.ForeignKey(DefoulMultitQuiz, on_delete=models.CASCADE,related_name='variants')
    is_true = models.BooleanField(default=False)
    body = models.TextField()

class DefoulMultitQuizAnswer(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='my_answer_default_multi_quiz')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='default_multi_quiz_answers')
    is_true = models.BooleanField(default=False)
    default_quiz = models.ForeignKey(DefoulMultitQuiz, on_delete=models.CASCADE,related_name='answers')



class ClosedTest(models.Model):
    body = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='my_closed_quizes')
    users = models.ManyToManyField(MyUser, related_name='accepted_closed_quizess', null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='default_closed_quizes')
    ball = models.FloatField(default=0.0)

    date_created = models.DateTimeField(auto_now=True)
    true_answer = models.CharField(max_length=100000000)
    
class ClosedTestAnswer(models.Model):
    is_true = models.BooleanField(default=False)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='closed_test_answers')
    answer = models.CharField(max_length=3234234234)
    closed_quiz = models.ForeignKey(ClosedTest, models.CASCADE, related_name='answers')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='default_closed_answers')

class Result(models.Model):
    user = models.ForeignKey(MyUser, models.CASCADE, related_name='quiz_result')
    score = models.FloatField(default=0.0)
    test = models.ForeignKey(Quiz, models.CASCADE, related_name='results')
    data = models.JSONField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)
    time = models.TimeField(null=True, blank=True)
    orin = models.IntegerField(default=1)

    def get_trues(self):
        return len([i for i, j in self.data.items() if j==True])
    
    def get_falses(self):
        return len([i for i, j in self.data.items() if j==False])


class StartedTime(models.Model):
    time = models.TimeField()
    started_time = models.TimeField(auto_now=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='strted_time')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='started_time_in_quiz')

    def total_seconds(self):
        hours, minutes, seconds = map(int, str(self.time).split(':'))
        return hours * 3600 + minutes * 60 + seconds

    def get_t_1(self):
        stt = str(self.started_time).split('.')[0]
        hours, minutes, seconds = map(int, str(stt).split(':'))
        return hours * 3600 + minutes * 60 + seconds