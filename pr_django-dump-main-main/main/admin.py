from django.contrib import admin
from .models import Task
from .models import Quiz

admin.site.register(Task)
admin.site.register(Quiz)