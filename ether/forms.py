from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import *
from .models import *

class RegisterForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class NewsletterForm(ModelForm):
    email = EmailField(max_length=254)

    class Meta:
        model = Newsletter
        fields = ["email"]

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = []

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'tags']

class ContactForm(Form):
    name = CharField(required=True)
    from_email = EmailField(required=True)
    subject = CharField(required=True)
    message = CharField(widget=Textarea, required=True)