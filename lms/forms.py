from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm, ValidationError
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2"]

class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender', 'birth_date', 'student_id']


class ModuleForm(ModelForm):
    class Meta:
        model = CourseModule
        fields = ['name', 'description', 'module_file']


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'multiple_choice']