from django.urls import path
from .views import (profile_update, ProfileDetailView,
                    register_user, login_user, logout_user,
                    password_reset_request, password_reset_confirm,
                    reset_done)


urlpatterns = [
    path("user/reset_done", reset_done, name='password_reset_done'),
    path("user/edit", profile_update, name='profile_edit'),
    path("user/<str:slug>/", ProfileDetailView.as_view(), name='profile_detail'),
    path("user/register", register_user, name='register'),
    path("user/login", login_user, name='login'),
    path("user/logout", logout_user, name='logout'),
    path("user/reset", password_reset_request, name='password_reset_request'),
    path("user/reset_confirm/<uidb64>/<token>/", password_reset_confirm, name='password_reset_confirm'),
]