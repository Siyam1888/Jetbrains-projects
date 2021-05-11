from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView


# Create your views here.
class UserSignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'base/signup.html'
    success_url = 'login'


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'base/login.html'


