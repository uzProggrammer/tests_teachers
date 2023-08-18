from django.contrib import admin
from .models import __all__

for i in __all__:
    admin.site.register(i)