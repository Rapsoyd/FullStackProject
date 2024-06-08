from django.views.generic import DetailView
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import make_password


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(reverse('password_reset_confirm', args=[uid, token]))
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'egorsamber323@gmail.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset link sent to your email.')
            return redirect('password_reset_done')
        else:
            messages.error(request, 'User with this email does not exists')
            return redirect('password_reset_request')
    return render(request, 'accounts/password_reset_request.html')


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if new_password1 and new_password2 and new_password1 == new_password2:
                user.password = make_password(new_password1)
                user.save()
                messages.success(request, 'Your password has been set. You can now log in.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'accounts/password_reset_confirm.html')
    else:
        messages.error(request, 'Password reset link is invalid or has expired.')
        return redirect('password_reset_request')


def reset_done(request):
    return render(request, 'accounts/password_reset_done.html')


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered')
            else:
                user = User.objects.create(username=username, email=email, password=password1)
                user.save()
                login(request, user)
                return redirect('blogs_page')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'accounts/register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blogs_page')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('blogs_page')  # Замените 'home' на имя вашей домашней страницы


class ProfileDetailView(DetailView):
    """
    Представление для просмотра профиля
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'accounts/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Профиль пользователя: {self.object.user.username}'
        return context


@login_required
def profile_update(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        bio = request.POST.get('bio')
        avatar = request.POST.get('avatar')

        if User.objects.filter(email=email).exclude(username=user.username).exists():
            context = {
                'error_message': 'Email адрес должен быть уникальным',
                'title': f"Редактирование профиля пользователя {user.username}"
            }
            return render(request, 'accounts/profile_edit.html', context)

        with transaction.atomic():
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if birth_date:
                profile.birth_date = birth_date
            profile.bio = bio
            if avatar:
                profile.avatar = avatar
            profile.save()

        return redirect(reverse_lazy('profile_detail', kwargs={'slug': profile.slug}))

    context = {
        'title': f"Редактирование профиля пользователя: {request.user.username}",
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'bio': profile.bio,
        'avatar': profile.avatar,
    }
    return render(request, 'accounts/profile_edit.html', context, )
