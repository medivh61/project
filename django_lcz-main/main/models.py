from email.policy import default
from django.db import models
import random
from django.contrib.auth.models import User
from django.forms import ImageField

#личный кабинет
#pip install pillow
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="ava1.jpg",null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

#создание теста
# Create your models here.
DIFF_CHOICES = (
        ('Простой', 'Простой'),
        ('Средний', 'Средний'),
        ('Сложный', 'Сложный'),
    )

class Quiz(models.Model):
    name = models.CharField(max_length = 120)
    topic = models.CharField(max_length = 120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="Время теста в минутах")
    reqired_score_to_pass = models.IntegerField(help_text="Необходимый балл для прохождения в %")
    difficulty = models.CharField(max_length = 7, choices = DIFF_CHOICES)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]
    
    class Meta:
        verbose_name_plural = 'Quizes'

#создание карточек
class Task(models.Model):
    title = models.CharField('Слово', max_length=50)
    task = models.CharField('Перевод', max_length=50)

    def __str__(self): #Вывод на экран объект класса
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

