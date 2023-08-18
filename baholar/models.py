from django.db import models
from users.models import MyUser
from assignments.models import Assignment
from bsb.models import BSB

class Baho(models.Model):
    user = models.ForeignKey(MyUser, related_name='baholar', on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='bahocalar', null=True, blank=True)
    bsb = models.ForeignKey(BSB, on_delete=models.CASCADE, related_name='baholarr', null=True,
                                   blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    baholar = (
        ('5','5'),
        ('4','4'),
        ('3','3'),
        ('2','2'),
        ('1','1'),
        ('0','0'),
        ('DQ', 'Darsda qatnashmadi'),
        ('BO', 'Baho olmadi')

    )
    baho = models.CharField(max_length=40, choices=baholar)

    def __str__(self):
        return f'{self.user} {self.baho} oldi.'