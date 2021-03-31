from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import *
from .models import *

class RegisterForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class NewsletterForm(ModelForm):
    email = EmailField(max_length=254)

    class Meta:
        model = Newsletter
        fields = ["email"]

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'tags']