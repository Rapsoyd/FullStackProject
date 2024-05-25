from django.urls import path
from .views import ProfileUpdateView, ProfileDetailView, register, login, logout

urlpatterns = [
    path("user/edit", ProfileUpdateView.as_view(), name='profile_edit'),
    path("user/<str:slug>/", ProfileDetailView.as_view(), name='profile_detail'),
    path("user/register", register, name='register'),
    path("user/login", login, name='login'),
    path("user/logout", logout, name='logout'),
]