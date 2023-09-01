from django.db import models
from users.models import MyUser
from .complier.main import Complier
import time as defaul_time

class Masala(models.Model):
    class Ball(models.IntegerChoices):
        Boshlangich = 10
        ASOSIY = 30
        NORMAL = 70
        ORTA = 150
        ILGOR = 400
        QIYIN = 1000
        EXTREMAL = 2500

    class Difficulty(models.IntegerChoices):
        BEGINNER = 1
        BASIC = 2
        NORMAL = 3
        MEDIUM = 4
        ADVANCED = 5
        HARD = 6
        EXTREMAL = 7
        FOR_EXPERT = 8


    diffs = (
        (1, 1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
        (6,6),
        (7,7),
        (8,8)
    )
    difficulty = models.IntegerField(choices=diffs, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    time_limit = models.PositiveIntegerField(default=1000)
    memory_limit = models.PositiveIntegerField(default=6)
    title = models.CharField(max_length=1000)
    body = models.TextField()
    slug = models.SlugField(max_length=40)
    info_in = models.TextField(null=True, blank=True)
    out = models.TextField(null=True, blank=True)
    checker = models.TextField(null=True, blank=True)
    types = (
        ('masala', 'masala'),
        ('bir qator', 'bir qator'),
        ('bitta urinish', 'bitta urinish'),
    )
    type = models.CharField(max_length=40, choices=types, default='masala')

    is_archived = models.BooleanField(default=False)

    yechim = models.TextField(null=True, blank=True)
    have_yechim = models.BooleanField(default=False)

    empty = models.BooleanField(default=True)

    accepteds = models.ManyToManyField(MyUser, related_name='masala_accepts', null=True, blank=True)
    wrong_answers = models.ManyToManyField(MyUser, related_name='masala_wrongs', null=True, blank=True)


    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='masalarim')
    korinadigan_testlar = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.title

    def get_diff(self):
        diff = 'Boshlang\'ich' if self.difficulty == 1 else 'Asoslar' if self.difficulty == 2 else 'Normal' if self.difficulty==3 else 'O\'rtacha' if self.difficulty==4 else 'Ilg\'or' if self.difficulty == 5 else 'Qiyin' if self.difficulty==6 else 'Juda Qiyin' if self.difficulty == 7 else 'Ekspert uchun' if self.difficulty==8 else ''
        return diff

    def get_diff_color(self):
        diff = 'rgb(20,110,20)' if self.difficulty == 1 else 'rgb(60, 116, 146)' if self.difficulty == 2 else 'rgb(90,90,190)' if self.difficulty==3 else 'rgb(106, 90, 205)' if self.difficulty==4 else 'rgb(125, 85, 9)' if self.difficulty == 5 else 'rgb(220, 73, 73)' if self.difficulty==6 else 'rgb(36, 35, 35)' if self.difficulty == 7 else 'rgb(1,1,1)' if self.difficulty==8 else ''
        return diff

    def get_1_teg(self):
        return [i.tag.name for i in self.tegs.all()] if self.tegs else []

    def get_2_teg(self):
        return [i.tag.name for i in self.tegs.all()][:3] if self.tegs else []

    def get_simple_tests(self):
        return self.testlar.all()[:self.korinadigan_testlar] if self.testlar.count() >= self.korinadigan_testlar else self.testlar.all()[:1] if self.testlar.count() > 0 else False

    def run(self, username, lang, urinish):
        self.empty = False
        self.save()
        time = int()
        memory = int()
        data1 = {}
        i = 1
        d='Qabul Qilindi'
        for test in self.testlar.all():
            urinish.turi = f'Tekshirilmoqda {i}'
            urinish.save()
            data = Complier(body=urinish.body, time_limit=self.time_limit, memory_limit = self.memory_limit, username=username, _in=test.t_in, out=test.out, checker=self.checker if self.checker else None, lang=urinish.til)
            data = data.run()
            urinish.time = data['time']
            urinish.memory = data['memory']
            if 'e' in data:
                urinish.error = data['e']
                urinish.save()
            if data['time']>time:
                time = data['time']
            if data['memory']>memory:
                memory = data['memory']
            data1[i] = data
            d='Qabul Qilindi'
            if data['status'] != 'Qabul qilindi':
                data1[i] = {
                    'status': f'{data["status"]} {i}',
                    'memory': data['memory'],
                    'time': data['time']
                }
                d=f'{data["status"]} {i}'
                break
            data1[i] = data
            i+=1
        urinish.tests = data1
        urinish.memory = memory
        urinish.time = time
        urinish.turi = d
        urinish.save()
        self.empty = True
        user = MyUser.objects.get(username=username)
        if d=='Qabul Qilindi':
            self.accepteds.add(user)
            if user in self.wrong_answers.all():
                self.wrong_answers.remove(user)
        else:
            if user not in self.accepteds.all():
                self.wrong_answers.add(user)
        self.save()
        return urinish

    def get_likes(self):
        return self.lieks.filter(type='like').count()

    def get_dislikes(self):
        return self.lieks.filter(type='dislike').count()


class Testlar(models.Model):
    t_in = models.TextField(max_length=100000000000)
    out = models.TextField(max_length=100000000000)
    masala = models.ForeignKey(Masala, on_delete=models.CASCADE, related_name='testlar')

class Urinish(models.Model):
    tests = models.JSONField(null=True, blank=True)
    turi = models.CharField(max_length=100)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='masala_urinishlari')
    masala = models.ForeignKey(Masala, on_delete=models.CASCADE, related_name='urinishlar')
    time = models.CharField(max_length=3423)
    memory = models.CharField(max_length=34234)
    olcham = models.IntegerField()
    tillar = (
        ('python', 'python'),
        ('node', 'node'),
    )
    til = models.CharField(max_length=213, choices=tillar)
    body = models.TextField(blank=True, null=True)
    error = models.TextField(default=None, null=True, blank=True)


class Teg(models.Model):
    name = models.CharField(max_length=50)


class MasalaTeg(models.Model):
    problem = models.ForeignKey(
        Masala,
        on_delete=models.CASCADE,
        related_name='tegs'
    )
    tag = models.ForeignKey(Teg, on_delete=models.CASCADE)


class Likelar(models.Model):
    types = (
        ('like', 'like'),
        ('dislike', 'dislike'),
    )
    type = models.CharField(choices=types, max_length=3234)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='masala_like')
    masala = models.ForeignKey(Masala, on_delete=models.CASCADE, related_name='lieks')
