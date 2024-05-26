from django.urls import path
from .views import ProfileUpdateView, ProfileDetailView, register_user, login_user, logout_user

urlpatterns = [
    path("user/edit", ProfileUpdateView.as_view(), name='profile_edit'),
    path("user/<str:slug>/", ProfileDetailView.as_view(), name='profile_detail'),
    path("user/register", register_user, name='register'),
    path("user/login", login_user, name='login'),
    path("user/logout", logout_user, name='logout'),
]