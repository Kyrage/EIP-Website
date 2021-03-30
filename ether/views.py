from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as dj_login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from .models import *
from .forms import *


def handler401(request):
    """Error management 401 unauthorized\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Http response with html page that displays error 401 without data
    """
    context = {}
    return render(request, 'errors/401.html', context)

def handler404(request, exception):
    """Error management 404 page not found\n\n
    :param [request]: Receives an HttpRequest
    :param [exception]: Cause of the error returned by django
    :type [request]: HttpRequest
    :type [exception]: string
    :return: Http response with html page that displays error 404 without data
    """
    context = {}
    return render(request, 'errors/404.html', context)

def handler500(request):
    """Error management 500 internal server error\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Http response with html page that displays error 500 without data
    """
    context = {}
    return render(request, 'errors/500.html', context)

def register(request):
    if request.user.is_authenticated:
        messages.warning(request, "Warning: You're already authenticated")
        return redirect('home')
    else:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                username = form.cleaned_data.get('username')
                current_site = get_current_site(request)
                mail_subject = 'Activate your Ether account.'
                message = render_to_string('registration/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                messages.success(request, "Account was created for " + username + " don't forget to activate it by email")
                return redirect("login")
        else:
            form = RegisterForm()
    context = {"form": form}
    return render(request, "registration/login.html", context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        dj_login(request, user)
        messages.success(request, 'Thank you for your email confirmation.')
        return redirect('home')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "Warning: You're already authenticated")
        return redirect('home')
    else:
        return render(request, 'registration/login.html', locals())

@login_required(login_url='login')
def profile(request):
    if request.user.has_usable_password() == False:
        messages.error(request, 'You are connected with OAuth2 you cannot change your password')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context = {"form": form}
    return render(request, 'registration/profile.html', context)

def home(request):
    context = {}
    return render(request, 'index.html', context)

def games(request):
    context = {}
    return render(request, 'games.html', context)

@login_required(login_url='login')
def alpha(request):
    context = {}
    return render(request, '', context)

@login_required(login_url='login')
def beta(request):
    context = {}
    return render(request, '', context)

def news(request):
    context = {}
    return render(request, 'blog.html', context)

def contact(request):
    context = {}
    return render(request, 'contact.html', context)
