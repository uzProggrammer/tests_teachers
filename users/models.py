from django.db import models
from django.contrib.auth.models import AbstractUser
from apiv1.naturaltime import naturaltime
from django.utils import timezone
from datetime import timedelta
from django.core import validators
from django.utils.deconstruct import deconstructible
import re

@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    regex = r"^[\w_]+\Z"
    flags = re.ASCII


class MyUser(AbstractUser):
    username_validator = ASCIIUsernameValidator()
    fanlar = (
        ('Matematika', 'Matematika'),
        ('ona_tili', 'Ona Tili'),
        ('musiqa', 'Musiqa'),
        ('rus_tili', 'Rus tili'),
        ('english', 'Chet tili'),
        ('jismoniy_tarbiya', 'Jismoniy tarbiya'),
        ('tarix', 'Tarix'),
        ('geografiya', 'Geografiya'),
        ('tasviriy_sanat', 'Tasviriy san\'at'),
        ('informatika', 'Informatika'),
        ('direktor', 'Direktor'),
        ('urin_bosar', 'Direktor o\'rin bosari'),
        ('psixolog', 'Psixolog'),
        ('maslahatchi', 'Maslahatchi'),
        ('chqbt', 'Chqbt'),
        ('kutubxonaxhi', 'Kutubxona'),
        ('biologiya', 'Biologiya'),
        ('kimyo', 'Kimyo'),
        ('huquq', 'Huquq'),
        ('fizika', 'Fizika'),
        ('texnologiya', 'Texnologiya'),
        ('iqtisod', 'Iqtisod')
    )
    is_teacher = models.BooleanField(default=False)
    fan = models.CharField(max_length=30, choices=fanlar, blank=True, null=True)

    sinflar = (
        ('5.1', '5.1'),
        ('5.2', '5.2'),
        ('6.1', '6.1'),
        ('6.2', '6.2'),
        ('7.1', '7.1'),
        ('7.2', '7.2'),
        ('7.3', '7.3'),
        ('8.1', '8.1'),
        ('8.2', '8.2'),
        ('8.3', '8.3'),
        ('9.1', '9.1'),
        ('9.2', '9.2'),
        ('9.3', '9.3'),
        ('10.1', '10.1'),
        ('10.2', '10.2'),
        ('10.3', '10.3'),
        ('11.1', '11.1'),
        ('11.2', '11.2'),
        ('11.3', '11.3'),
        ('Guest', 'Guest'),
    )
    is_student = models.BooleanField(default=True)
    sinf = models.CharField(max_length=30, choices=sinflar, blank=True, null=True)
    themes = (
        ('default', 'dark'),
        ('light', 'light'),
        ('green', 'green'),
        ('black', 'black'),
        ('brown', 'brown'),
    )
    navbar_colors = (
        ('light', 'light'),
        ('blue', 'blue'),
        ('green', 'green'),
        ('brown', 'brown'),
        ('black', 'black'),
    )

    last_visit = models.DateTimeField(null=True, blank=True)

    font = models.CharField(max_length=30, default='sans-serif')
    navbar_color = models.CharField(max_length=30, choices=navbar_colors, default='blue')
    ball = models.FloatField(default=0.0)
    theme = models.CharField(max_length=30, choices=themes, default='light')
    bio = models.TextField(default='.')
    friends = models.ManyToManyField('self',related_name='user_friends', blank=True, null=True)

    is_create_course = models.BooleanField(default=False)
    is_create_test = models.BooleanField(default=False)
    is_create_ass = models.BooleanField(default=False)
    is_create_masala = models.BooleanField(default=False)
    is_create_yechim = models.BooleanField(default=False)
    is_create_bsb = models.BooleanField(default=False)

    def status(self):
        now = timezone.now()
        
        now_10 = now - timedelta(minutes = 1)
        if now_10 < self.last_visit < now:
            return 'Online'
        return naturaltime(self.last_visit)