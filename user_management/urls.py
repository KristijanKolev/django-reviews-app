from django.urls import path

from . import views

app_name = 'user_management'

urlpatterns = [
    path('login', views.basic_login, name='login'),
    path('logout', views.logout_view, name='logout'),
]