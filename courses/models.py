from django.db import models
from users.models import MyUser
import random

class CourseTag(models.Model):
    title = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=10000)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='courses')

    users = models.ManyToManyField(MyUser, related_name='followed_courses', null=True, blank=True)
    tags = models.ManyToManyField(CourseTag, related_name='courses', null=True, blank=True)

    summary = models.CharField(max_length=555555)
    about = models.TextField()
    is_public = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

class CourseComment(models.Model):
    body = models.TextField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='course_comments')
    date_created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self) -> str:
        return f'{self.user.username} {self.course.title}ga izoh yozdi'

class Lessons(models.Model):
    title = models.CharField(max_length=324234)
    summary = models.CharField(max_length=99999999999)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    slug = models.SlugField(max_length=64)
    def __str__(self) -> str:
        return self.title



class DragAndDropQuiz(models.Model):
    slug = models.SlugField(default='asfdf')
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='drag_and_drop')
    body = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='drag_and_drop_quizes')
    users = models.ManyToManyField(MyUser, null=True, blank=True)

    def get_keys(self):
        keys = self.variants.all().order_by('?')
        d = []
        for i in keys:
            if not i.key:
                d.append(i)
        return d
    
    def get_values(self):
        keys = self.variants.all().order_by('?')
        d = []
        for i in keys:
            if not i.key:
                pass
            else:
                d.append(i)
        return d

class DragAndDropVariant(models.Model):
    quiz = models.ForeignKey(DragAndDropQuiz, on_delete=models.CASCADE, related_name='variants')
    body = models.TextField()
    key = models.ForeignKey('self', on_delete=models.CASCADE, related_name='value', null=True, blank=True)

class DragAndDropAnswer(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    test = models.ForeignKey(DragAndDropQuiz, on_delete=models.CASCADE, related_name='answer')
    is_true = models.BooleanField(default=False)
    answer = models.CharField(max_length=99999999999999)
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='course_drag_anddrop_answers')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_draganddrop_answers')
    


class Lectures(models.Model):
    body = models.TextField()
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='lektures')
    users = models.ManyToManyField(MyUser, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    slug = models.SlugField(default='asfdf')




class CourseYopiqTest(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    body = models.TextField()
    answer = models.CharField(max_length=1000000000)
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='yopiq_tests')
    slug = models.SlugField(default='asfdf')

    users = models.ManyToManyField(MyUser, null=True, blank=True)

class YopiqTestAnswer(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    test = models.ForeignKey(CourseYopiqTest, on_delete=models.CASCADE, related_name='yopiqtestanswer')
    is_true = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_yopiqtest_answers')
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='course_yopiq_test_answers')
    answer = models.CharField(max_length=324234235423)


class CourseQuiz(models.Model):
    body = models.TextField()
    lesson = models.ForeignKey(Lessons,on_delete=models.CASCADE, related_name='quizes')
    users = models.ManyToManyField(MyUser, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizess')
    slug = models.SlugField(default='asfdf')

    def get_random(self):
        variants = self.variants
        return variants.order_by('?')

class CourseQuizVariant(models.Model):
    body = models.TextField()
    is_true = models.BooleanField(default=False)
    quiz = models.ForeignKey(CourseQuiz, on_delete=models.CASCADE, related_name='variants')

class QuizAnswer(models.Model):
    is_true = models.BooleanField(default=False)
    quiz = models.ForeignKey(CourseQuiz, on_delete=models.CASCADE, related_name='answers')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_quiz_answer')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='course_quiz_answers')
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='course_quiz_answer')
    variant = models.ForeignKey(CourseQuizVariant, on_delete=models.CASCADE, related_name='answers')


class CourseMultiQuiz(models.Model):
    slug = models.SlugField(default='asfdf')
    body = models.TextField()
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='multi_quizes')
    users = models.ManyToManyField(MyUser, null=True,blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='multi_quizess')

    def quizes(self):
        return self.variants.all().order_by('?')

class MultiQuizVariuant(models.Model):
    quiz = models.ForeignKey(CourseMultiQuiz, on_delete=models.CASCADE, related_name='variants')
    is_true = models.BooleanField(default=False)
    body = models.TextField()

class MultiQuizAnswer(models.Model):
    quiz = models.ForeignKey(CourseMultiQuiz, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='course_multiquiz_answers')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_multiquiz_answer')
    is_true = models.BooleanField(default=False)
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='course_multiquiz_answer')
    variants = models.ManyToManyField(MultiQuizVariuant, related_name='answers', null=True, blank=True)

__all__ = [
    Course,
    CourseTag,
    Lessons,
    DragAndDropQuiz,
    DragAndDropVariant,
    DragAndDropAnswer,
    Lectures,
    CourseYopiqTest,
    YopiqTestAnswer,
    CourseQuiz,
    CourseQuizVariant,
    QuizAnswer,
    CourseMultiQuiz,
    MultiQuizVariuant,
    MultiQuizAnswer,
]