import imp
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


from .views import(
    QuizListView,
    quiz_view,
    quiz_data_view,
    save_quiz_view,
)

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('makecard', views.make_card, name='makecard'),
    path('learncard', views.learn_cards, name='learncard'),
    path('listening', views.listening, name='listening'),

    path('readcz', views.reading_cz, name='readcz'),
    path('readcz1', views.reading1, name='readcz1'),
    path('readcz2', views.reading2, name='readcz2'),
    path('readcz3', views.reading3, name='readcz3'),

    path('register', views.registration, name='register'),
    path('login', views.loginpage, name='login'),
    path('logout', views.logoutUser, name='logout'),

    path('lk', views.lkUsers, name='lk'),

    path('memorygame', views.memory, name="memorygame"),

    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('accounts/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    #path('reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_confirm'),

    path('main-view/', QuizListView.as_view(), name='main-view'),
    path('main-view/<int:pk>', quiz_view, name='quiz-view'),
    path('main-view/<int:pk>/save/', save_quiz_view, name = 'save-view'),
    path('main-view/<int:pk>/data/', quiz_data_view, name='quiz-data-view'),

]
