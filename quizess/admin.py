from django.contrib import admin
from .models import *

admin.site.register(Task)
admin.site.register(TaskQuestion)
admin.site.register(QuestionAnswers)
admin.site.register(Result)