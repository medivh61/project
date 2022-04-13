from django.http import HttpResponse
from django.shortcuts import redirect

#использовать как @unauthenticated_user во views
def unauthenticated_user(view_func): #вход только для незареганных пользователей
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return wrapper_func


#использовать как @allowed_users(allowed_roles=['название группы']) во views
def allowed_users(allowed_roles=[]): #вход только конкретной группе пользователей(например админ)
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Для просмотра этой странницы необходимо авторизоваться')
        return wrapper_func
    return decorator


#использовать как @admin_only во views
#вход только админам (эквивалентно @allowed_users(allowed_roles=['admin']))
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('home')
        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_func