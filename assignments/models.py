from django.db import models
from users.models import MyUser
from ckeditor.fields import RichTextField

class Assignment(models.Model):
    author = models.ForeignKey(MyUser, related_name='assignment_author', on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    info = RichTextField()

    sinf = models.CharField(max_length=50, null=True, blank=True, )

    student = models.ForeignKey(MyUser, related_name='assignment_student', on_delete=models.CASCADE, null=True, blank=True)

    is_readed = models.BooleanField(default=False)
    qachongacha = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    javoblar=models.ManyToManyField(MyUser, related_name='topshirilgan_topshiriqlar', null=True, blank=True)
    max_ball = models.FloatField(default=2.0)

    def __str__(self):
        return self.title

class StudentAnswer(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='assigment_answer')
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='assignment_answers')
    answer = RichTextField()
    is_readed = models.BooleanField(default=False)
    yordam_berganlar = models.ManyToManyField(MyUser, related_name='student_answer_helpers', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(MyUser, related_name='student_answer_likes', null=True, blank=True)

    def __str__(self):
        return f'{self.student} answer for {self.assignment}'

class StudentAnswerComments(models.Model):
    student_answer = models.ForeignKey(StudentAnswer, on_delete=models.CASCADE, related_name='student_answer_comments')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='student_answer_comments_user')
    body = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(MyUser, related_name='student_answer_comments_likes', null=True, blank=True)

class StudentAnswerBall(models.Model):
    teacher = models.ForeignKey(MyUser, related_name='teacher_student_ball', on_delete=models.CASCADE)
    student_answer = models.ForeignKey(StudentAnswer, on_delete=models.CASCADE, related_name='student_answer_ball')
    ball = models.FloatField()
    is_readed = models.BooleanField(default=False)
    xatolar_va_kamchiliklar = RichTextField(null=True, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='assigment_answer_balls')
    date_created = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(MyUser, related_name='teacher_ball_likes', null=True, blank=True)

class StudentAnswerBallComment(models.Model):
    student_answer_ball = models.ForeignKey(StudentAnswerBall, on_delete=models.CASCADE, related_name='student_answer_ball_comment')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='student_answer_ball_comment_user')
    body = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(MyUser, related_name='student_answer_ball_comment_likes', null=True, blank=True)