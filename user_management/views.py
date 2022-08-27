from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction

from .forms import LoginForm, RegisterUserForm
from .models import Profile


def basic_login(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        context['form'] = form
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(form.cleaned_data['success_redirect_url'])
            else:
                context['error_message'] = 'Username or password incorrect!'
        else:
            context['error_message'] = 'Invalid input data!'
    else:
        form = LoginForm(initial={'success_redirect_url': request.GET.get('next', '/')})
        context['form'] = form

    return render(request, 'user_management/login.html', context=context)


@transaction.atomic
def user_signup(request):
    context = {}
    if request.method == 'POST':
        form = RegisterUserForm(data=request.POST, files=request.FILES)
        context['form'] = form
        if form.is_valid():
            new_user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'])
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            profile = Profile(user=new_user, bio=form.cleaned_data.get('bio'))
            uploaded_image = request.FILES.get('profile_picture')
            if uploaded_image is not None:
                file_type_extension = uploaded_image.name.split('.')[-1]
                uploaded_image.name = f'pp_{new_user.username}.{file_type_extension}'
                profile.profile_picture = uploaded_image
            profile.save()

            login(request, new_user)

            return HttpResponseRedirect(reverse('reviews:places_all'))

    else:
        context['form'] = RegisterUserForm()

    return render(request, 'user_management/signup.html', context=context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_management:login'))
