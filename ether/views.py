from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as dj_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.db.models.signals import post_save
from taggit.models import Tag
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail, BadHeaderError
from .tokens import *
from .models import *
from .forms import *

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def initNewsletter(sender, instance=None, created=False, **kwargs):
    if created:
        newsletter = Newsletter.objects.create(author=instance)
        newsletter.publish()

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
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            obj, created = Game.objects.update_or_create(author=request.user)
            if created:
                obj.alpha = True
                obj.edit()
                messages.success(request, "You are now registered to Alpha!")
            else:
                obj.author = request.user
                obj.alpha = True
                obj.publish()
                messages.success(request, "You are now registered to Alpha!")
        else:
            messages.warning(request, "An Error occured please try again!")
    else:
        form = GameForm()
    try:
        x = Game.objects.get(author=request.user)
        x = x.alpha
    except:
        x = False
    context = {'alpha': x}
    return render(request, 'alpha.html', context)

@login_required(login_url='login')
def beta(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            obj, created = Game.objects.update_or_create(author=request.user)
            if created:
                obj.beta = True
                obj.edit()
                messages.success(request, "You are now registered to Beta!")
            else:
                obj.author = request.user
                obj.beta = True
                obj.publish()
                messages.success(request, "You are now registered to Beta!")
        else:
            messages.warning(request, "An Error occured please try again!")
    else:
        form = GameForm()
    try:
        x = Game.objects.get(author=request.user)
        x = x.beta
    except:
        x = False
    context = {'beta': x}
    return render(request, 'beta.html', context)

def news(request):
    posts = Post.objects.order_by('-created_date', '-last_edit')
    common_tags = Post.tags.most_common()[:4]
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.title = form.cleaned_data["title"]
            newpost.description = form.cleaned_data["description"]
            newpost.slug = slugify(newpost.title)
            newpost.publish()
            form.save_m2m()
            messages.success(request, "Post added!")
        else:
            print(form)
            messages.warning(request, "The field isn't valid!")
    else:
        form = PostForm()
    context = {'posts': posts, 'common_tags': common_tags, 'form': form}
    return render(request, 'blog.html', context)

def specificNews(request, id):
    post = get_object_or_404(Post, id=id)
    context = {'post': post}
    return render(request, 'detail.html', context)

def tagged(request, id):
    tag = get_object_or_404(Tag, id=id)
    posts = Post.objects.filter(tags=tag)
    context = {'tag': tag, 'posts': posts}
    return render(request, 'blog.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message'] + str(" de {0}".format(name))
            try:
                send_mail(subject, message, from_email, ['tristan.mesurolle@epitech.eu'])
                messages.success(request, "Message sent successfully!")
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact')
        else:
            messages.warning(request, "The field isn't valid!")
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'contact.html', context)

def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['author']
            obj, created = Newsletter.objects.update_or_create(author=email)
            if created:
                obj.registered = True
                obj.edit()
                messages.success(request, "You are now registered to the newsletter!")
            else:
                obj.author = email
                obj.registered = True
                obj.publish()
                messages.success(request, "You are now registered to the newsletter!")
        else:
            messages.warning(request, "The field isn't valid!")
    else:
        form = NewsletterForm()
    return redirect('profile')