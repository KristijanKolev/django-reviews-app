from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse


def basic_login(request):
    context = {}
    if request.method == 'POST':
        success_redirect_url = request.POST.get('success_redirect_url', '/')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(success_redirect_url)
        else:
            context['error_message'] = 'Username or password incorrect!'
    else:
        context['success_redirect_url'] = request.GET.get('next', '/')

    return render(request, 'user_management/login.html', context=context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_management:login'))
