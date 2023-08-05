from django.urls import path
from . import views

app_name = 'medicio'

urlpatterns = [
    # robots.txt는 반드시 가장 먼저
    path('robots.txt', views.robots),
    path('', views.home, name='home'),
]
