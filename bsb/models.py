from random import choices

from ckeditor.fields import RichTextField
from django.db import models

from sinflar.models import Sinf
from users.models import MyUser




class BSB(models.Model):
    title = models.CharField(max_length=50)
    date_statrted = models.DateTimeField()
    date_ended = models.DateTimeField()
    actioned_users = models.ManyToManyField(MyUser, related_name='user_action_BSB', null=True, blank=True)
    holatlar = (
        ('Tugagan', 'Tugagan'),
        ('Boshlanmagan', 'Boshlanmagan'),
        ('Dovom etmoqda', 'Dovom etmoqda'),
    )
    types = (
        ('Masala', 'Masala'),
        ('Topshiriq', 'Topshiriq'),
        ('Test', 'Test')
    )

    type = models.CharField(max_length=20, choices=types, default='Topshiriq')
    holati = models.CharField(max_length=20, default='Boshlanmagan', choices=holatlar, null=True, blank=True)
    sinf = models.ForeignKey(Sinf, related_name='sinf_BSBs', on_delete=models.CASCADE)
    body = RichTextField()
    author = models.ForeignKey(MyUser, related_name='author_BSB', on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class BsbProblem(models.Model):
    bsb = models.ForeignKey(BSB, related_name='problems', on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='own_problems')
    title = models.CharField(max_length=150)
    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=16)
    difficulty = models.IntegerField(default=1)
    about = RichTextField()
    info_out = models.TextField(blank=True, null=True)
    info_in = models.TextField(blank=True, null=True)
    simple_tests = models.JSONField()
    tests = models.JSONField()
    yechim = models.TextField(blank=True, null=True, )
    date_created = models.DateTimeField(auto_now_add=True)
    accepteds = models.ManyToManyField(MyUser, related_name='accepted_problems', null=True, blank=True)
    foiz = models.FloatField(default=0)
    wrong_answers = models.ManyToManyField(MyUser, related_name='wrong_problems', null=True, blank=True)
    ball = models.FloatField()
    def __str__(self):
        return self.title

class BsbProblemAnswer(models.Model):
    body = models.TextField()
    type = models.CharField(max_length=30)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='bsb_task_answers')
    bsb_problem = models.ForeignKey(BsbProblem, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return f'{self.user.username} attempt {self.bsb_problem.title}'

class BsbProblemBall(models.Model):
    bsb_problem_answer = models.ForeignKey(BsbProblemAnswer, on_delete=models.CASCADE, related_name='balls')
    ball = models.FloatField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='bsb_problem_balls')
    def __str__(self):
        return f'{self.user.username} {self.bsb_problem_answer.bsb_problem.title}dan {self.ball} ball oldi.'


class BsbAssignment(models.Model):
    author = models.ForeignKey(MyUser, related_name='bsb_assignment_author', on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    info = RichTextField()
    ball = models.FloatField()
    is_readed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    Bsb = models.ForeignKey(BSB, on_delete=models.CASCADE, related_name='assignments')
    max_ball = models.FloatField(default=2.0)

    def __str__(self):
        return f'{self.author.username} {self.title} ni yaratdi.'

class StudentAnswer(models.Model):
    body = RichTextField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='bsb_assignment_answers')
    assignment = models.ForeignKey(BsbAssignment, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return f'{self.user.username} {self.assignment.title} ga javob qaytardi.'

class StudentAnswerBall(models.Model):
    ball = models.FloatField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='bsb_assignment_answer_balls')
    student_answer = models.ForeignKey(StudentAnswer, on_delete=models.CASCADE, related_name='answer_balls')
    bsb = models.ForeignKey(BSB, on_delete=models.CASCADE, related_name='assignment_balls')
    class Meta:
        ordering = ('-ball', )
    def __str__(self):
        return f'{self.user.username} {self.student_answer.assignment.title} dan {self.ball} oldi.'


class BsbQuiz(models.Model):
    q_id = models.IntegerField(default=0)
    bsb = models.ForeignKey(BSB, related_name='quizess', on_delete=models.CASCADE)
    body = RichTextField()
    ball = models.FloatField()
    def __str__(self):
        return self.body

class BsbQuizTests(models.Model):
    question = models.ForeignKey(BsbQuiz, on_delete=models.CASCADE, related_name='tests')
    body = RichTextField()
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.body

class BsbQuizBall(models.Model):
    quizess = models.ManyToManyField(BsbQuizTests, related_name='quiz_answers')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='bsb_quiz_ball')
    test = models.ForeignKey(BSB, on_delete=models.CASCADE, related_name="balls")
    scope = models.FloatField()

    def __str__(self):
        return str(self.pk)

class Yakuniy(models.Model):
    ball = models.FloatField(null=True, blank=True)
    bsb = models.ForeignKey(BSB, on_delete=models.CASCADE, related_name='yakuniy')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='yakuniy_baho_contorls')
    assignments = models.ManyToManyField(BsbAssignment, related_name='yakuniy_ball', null=True, blank=True)
    problem = models.ManyToManyField(BsbProblem, related_name='yakuniy_balls', null=True, blank=True)

    def __str__(self):
        return f'{self.user} {self.bsb}dan yakuniy bahosi {self.ball}'

__all__ = [
    BSB,
    BsbProblem,
    BsbProblemAnswer,
    BsbProblemBall,
    BsbAssignment,
    StudentAnswer,
    StudentAnswerBall,
    BsbQuiz,
    BsbQuizTests,
    BsbQuizBall,
    Yakuniy
]