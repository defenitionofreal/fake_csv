from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout')
]