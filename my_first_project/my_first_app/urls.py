from django.urls import path
from . import views

#3
urlpatterns=[
    path('',views.Home,name='home')
]