from django.urls import path
from . import views

urlpatterns = [
    path('', views.pong_view, name='pong_view'),
]
