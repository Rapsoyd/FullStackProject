from django import forms
from django.contrib.auth.models import User
from apps.accounts.models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

UPDATE_FORM_WIDGET = forms.TextInput(attrs={'class': 'form-control mb-1'})


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    password = forms.CharField(attrs=forms.PasswordInput, label='Ваш пароль')


class UserUpdateForm(forms.ModelForm):
    """
    Форма обновления данных пользователя
    """
    username = forms.CharField(max_length=100, widget=UPDATE_FORM_WIDGET)
    email = forms.EmailField(widget=UPDATE_FORM_WIDGET)
    first_name = forms.CharField(max_length=100, widget=UPDATE_FORM_WIDGET)
    last_name = forms.CharField(max_length=100, widget=UPDATE_FORM_WIDGET)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        """
        Проверка email на уникальность
        """
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError("Email адрес должен быть уникальным")
        return email


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма обновления данных пользователем
    """
    slug = forms.CharField(max_length=100, widget=UPDATE_FORM_WIDGET)
    birth_date = forms.DateField(widget=UPDATE_FORM_WIDGET)
    bio = forms.CharField(max_length=500, widget=UPDATE_FORM_WIDGET)
    avatar = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control mb-1"}))

    class Meta:
        model = Profile
        fields = ('slug', 'birth_date', 'bio', 'avatar')
