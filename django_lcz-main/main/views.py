from asyncio import tasks
import email
import re
from time import time
from tkinter.messagebox import QUESTION
from tkinter.tix import Tree
from tokenize import group
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import unauthenticated_user, allowed_users, admin_only
from matplotlib.pyplot import text
from matplotlib.style import use

from .models import *
from .forms import TaskForm, CreateUserForm, CustomerForm

from .models import Quiz

from django.http import JsonResponse
from django.shortcuts import HttpResponse
from questions.models import Answer, Question
from results.models import Result
# Create your views here.
def index(request):
    tasks = Task.objects.all()
    return render(request, 'main/index.html', {'title': 'Добро пожаловать в LearnCzech!', 'tasks': tasks})

def about(request):
    return render(request, 'main/about.html')

def memory(request):
    return render(request, 'main/memorygame.html')

@login_required(login_url='login') #незареганный пользователь не может создавать карточки и будет возвращен на стр входа
def make_card(request):
    error = ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') #после отправки формы отправляет на начал стр
        else:
            error = 'Форма была неверной'

    form = TaskForm()
    context = {
        'form': form,
        'error': error,
    }

    return render(request, 'main/createtask.html', context)

@login_required(login_url='login') #запрещенно для незарег. пользователя
#@allowed_users(allowed_roles=['admin']) #доступ конкретной группе в джанго админке
def learn_cards(request):
    tasks = Task.objects.all()
    return render(request, 'main/learn_cards.html', {'tasks': tasks})

def reading_cz(request): 
    return render(request, 'main/readcz.html') #страницы раздела "чтение"
def reading1(request):
    return render(request, 'main/pagesforread/page1.html')
def reading2(request):
    return render(request, 'main/pagesforread/page2.html')
def reading3(request):
    return render(request, 'main/pagesforread/page3.html')
def listening(request):
    return render(request, 'main/listeningcz.html')

@login_required(login_url='login') #запрещенно для незарег. пользователя
#@allowed_users(allowed_roles=['customer']) #доступ конкретной группе в джанго админке
def lkUsers(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'main/lk.html', context)

@unauthenticated_user
def registration(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer') #после регистрации присваивается статус customer
            user.groups.add(group)
            Customer.objects.create(
                user = user,
                name = user.username,
                email = user.email,
            )

            messages.success(request, username + ", Вы успешно зарегистрированы!")
            return redirect('login')

    context = {'form':form}
    return render(request, 'main/register.html', context)

@unauthenticated_user
def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Логин или пароль неверные!')

        context = {}
        return render(request, 'main/login.html', context)

def logoutUser(request): 
    logout(request)
    return redirect('login')
    #return render(request, 'main/login.html')


class QuizListView(ListView):
    model = Quiz
    template_name = 'main/main_quiz.html'

def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'main/quiz.html', {'obj': quiz})

def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q):answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


# def is_ajax(request):
#     return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def save_quiz_view(request, pk):
    print(request.POST)
    # if is_ajax(request=request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
    # if request.is_ajax():
        data = request.POST
        print(type(data))
        questions = []
        data = request.POST
        # data = dict(data.list())
        # print(type(data)) 
        data_ = dict(data.lists())
        print(type(data_))
        print(data_)
        data_.pop('csrfmiddlewaretoken')
        print(data_)
        for k in data_.keys():
            print('key: ',k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100/ quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected !="":
                question_answers = Answer.objects.filter(question=q) 
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score +=1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                results.append({str(q): {'correct_answer': correct_answer,'answered': a_selected}})
            else:
                 results.append({str(q):'not answered'})

        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user,score = score_)

        if score_ >=quiz.reqired_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})
        
    # return JsonResponse({'text': 'works'})