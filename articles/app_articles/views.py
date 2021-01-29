from django.contrib.auth.models import Group
from django.http import HttpRequest
from django.shortcuts import render, HttpResponse, redirect
from django.template import Context, loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from app_articles.decorators import allowed_users
from app_articles.forms import NameForm, UserCreationForm, CreateUserForm, LoginUserForm
from app_articles.models import User

from django.contrib.auth import authenticate, login, logout


# Create your views here.
def example(request):
    return HttpResponse("Hello")


def register(request):
    pass


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            email = form.cleaned_data.get("email")

            user = User.objects.create_user(username, email, password)
            customer_group = Group.objects.get(name='Customer')
            user.groups.add(customer_group)
            # Or: my_group.user_set.add(user)

            # A message variable will be pushed into the context automatically, just once.
            messages.success(request, f"User {user} was succesfully created!")

            return redirect('login')
            # user = authenticate(username='john', password='secret')

        else:
            # A message variable will be pushed into the context automatically, just once.
            messages.error(request, "User was not created.")
            return render(request, 'app_articles/register.html', {'form': form})

    form = CreateUserForm()
    return render(request, 'app_articles/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        # form = LoginUserForm(request, data=request.POST)
        # if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password is not None:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Donde se guarda las sessions/cookies de login, es sessiondi?
                # Esta bien acceder a traves de request.COOKIES?
                login(request, user)
                return redirect('inside')
            else:
                messages.error(request, "Bad username or Password.")

    return render(request, 'app_articles/login.html')


def logout_view(request):
    if request.user.username:
        logout(request)
        return HttpResponse('You are not logged in anymore!')
    else:
        return HttpResponse('No user logged')


@login_required(login_url='login')
def inside(request):
    return HttpResponse('You are logged!')


@login_required(login_url='login')
@allowed_users(allowed_groups=['Customer'])
def only_customers(request):
    return HttpResponse('You are a customer!')


@login_required(login_url='login')
def bad_groups(request):
    return HttpResponse('You are not allowed!')

