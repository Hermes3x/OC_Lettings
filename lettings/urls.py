"""URL routes of the lettings application, under the 'lettings' namespace."""

from django.urls import path

from . import views

app_name = 'lettings'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:letting_id>/', views.letting, name='letting'),
]
