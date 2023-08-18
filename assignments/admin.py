from django.contrib import admin
from .models import *

admin.site.register(Assignment)
admin.site.register(StudentAnswer)
admin.site.register(StudentAnswerComments)
admin.site.register(StudentAnswerBall)
admin.site.register(StudentAnswerBallComment)