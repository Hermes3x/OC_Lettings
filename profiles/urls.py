"""URL routes of the profiles application, under the 'profiles' namespace."""

from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.profile, name='profile'),
]
