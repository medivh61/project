from django.contrib import admin
from .models import Task
from .models import Quiz
from .models import Customer

admin.site.register(Task)
admin.site.register(Quiz)
admin.site.register(Customer)