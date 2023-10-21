from django.contrib import admin
from django.urls import path, include
from accounts.views import UserCreateView, UserUpdateView, Auth, Logout, profile

urlpatterns = [
    path('login', Auth.as_view(), name='login'),
    path('register', UserCreateView.as_view(), name='register'),
    path('logout', Logout.as_view(), name='logout'),
    path('profile', profile, name='profile'),
    path('update/<int:pk>', UserUpdateView.as_view(), name='update'),
]
