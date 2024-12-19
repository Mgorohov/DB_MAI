from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import TrainingModel, FoodModel


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput({"class": "form-control", "placeholder": "Username"}),
    )
    password1 = forms.CharField(
        label=("Password"),
        widget=forms.PasswordInput(
            {"class": "form-control", "placeholder": "Password"}
        ),
    )
    password2 = forms.CharField(
        label=("Password"),
        widget=forms.PasswordInput(
            {"class": "form-control", "placeholder": "Password"}
        ),
    )


class AuthForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput({"class": "form-control", "placeholder": "Username"}),
    )
    password = forms.CharField(
        label=("Password"),
        widget=forms.PasswordInput(
            {"class": "form-control", "placeholder": "Password"}
        ),
    )


class TrainingForm(forms.ModelForm):
    class Meta:
        model = TrainingModel
        fields = ('title', 'description', 'calories', 'duration')
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название тренировки"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Описание тренировки"}),
            "calories": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Калории"}),
            'duration': forms.NumberInput(attrs={"class": "form-control", "placeholder": "Длительность тренировки (мин)"}),
        }
        error_messages = {
            "title": {
                "max_length": _("Указано слишком большое название тренировки."),
            },
        }


class FoodForm(forms.ModelForm):
    class Meta:
        model = FoodModel
        fields = ('title', 'description', 'calories')
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Блюдо"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Описание еды"}),
            "calories": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Калории"}),
        }
        error_messages = {
            "title": {
                "max_length": _("Указан слишком длинный заголовок."),
            },
        }