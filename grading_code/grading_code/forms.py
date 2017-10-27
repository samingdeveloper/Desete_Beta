from django import forms
from django.contrib.auth.models import User
from .models import Classroom, Quiz


class ClassroomForm(forms.ModelForm):

    class Meta:
        model = Classroom
        fields = ['name', 'year']


class QuizForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = ['quiz_title']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
