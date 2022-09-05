from django.contrib.auth import login as dj_login, update_session_auth_hash
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.contrib import messages
from django.db.models import Q
from taggit.models import Tag
from .tokens import *
from .models import *
from .forms import *
import sweetify

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Creation of a profile for each new user
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Saves the user instance when all processing is finished
    """
    instance.profile.save()

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
    :type [exception]: String
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
    """Registration function\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Redirection to the login page
    """
    if request.user.is_authenticated:
        sweetify.info(request, 'You are already logged in as {0}'.format(request.user), button='Ok', timer=5000)
        return redirect('home')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                associatedUsers = User.objects.filter(Q(email=email))
                if associatedUsers.exists():
                    sweetify.error(request, 'A user already uses this email address.', button='Ok', timer=5000)
                else:
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    username = form.cleaned_data.get('username')
                    currentSite = get_current_site(request)
                    mailSubject = 'Activate your Ether account.'
                    message = render_to_string('registration/activeEmail.html', {
                        'user': user,
                        'domain': currentSite.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':account_activation_token.make_token(user),
                        'protocol': 'http',
                    })
                    toEmail = form.cleaned_data.get('email')
                    email = EmailMessage(mailSubject, message, to=[toEmail])
                    email.send()
                    sweetify.success(request, "Account was created for {0} don't forget to activate it by email.".format(username), button='Ok', timer=5000)
                    return redirect("login")
        else:
            form = RegisterForm()
    context = {'form': form}
    return render(request, 'registration/login.html', context)

def activateAccount(request, uidb64, token):
    """User account activation\n\n
    :param [request]: Receives an HttpRequest
    :param [uid64]: Receives an String
    :param [token]: Receives an String
    :type [request]: HttpRequest
    :type [request]: String
    :type [request]: String
    :return: Redirection to the main page
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        dj_login(request, user)
        sweetify.success(request, 'Thank you for validating your email.', button='Ok', timer=5000)
        return redirect('home')
    else:
        sweetify.error(request, 'The activation link is invalid.', button='Ok', timer=5000)
        return redirect('home')

def login(request):
    """Redirection to the login page\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Redirection to the main page
    """
    if request.user.is_authenticated() == True:
        sweetify.info(request, 'You are already logged in as {0}'.format(request.user), button='Ok', timer=5000)
        return redirect('home')
    else:
        return render(request, 'registration/login.html', locals())

def resetPassword(request):
    """Reset password\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Redirection to the login page
    """
    if request.method == 'POST':
        passwordResetForm = PasswordResetForm(request.POST)
        if passwordResetForm.is_valid():
            email = passwordResetForm.cleaned_data['email']
            associatedUsers = User.objects.filter(Q(email=email))
            if associatedUsers.exists():
                for user in associatedUsers:
                    currentSite = get_current_site(request)
                    subject = 'Password reset request'
                    emailTemplateName = 'registration/resetEmail.html'
                    content = {
                        'email': user.email,
                        'user': user,
                        'domain': currentSite.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    object = render_to_string(emailTemplateName, content)
                    try:
                        send_mail(subject, object, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                        sweetify.success(request, 'Email to reset your password sent successfully.', button='Ok', timer=5000)
                    except BadHeaderError:
                        sweetify.error(request, 'Invalid header found.', button='Ok', timer=5000)
                    return redirect('login')
            else:
                sweetify.error(request, 'No user is linked to this email.', button='Ok', timer=5000)
    else:
        passwordResetForm = PasswordResetForm()
    context = {'form': passwordResetForm}
    return render(request, 'registration/login.html', context)

@login_required(login_url='login')
def profile(request):
    """Displaying profile page\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Rendering profile page
    """
    user = get_object_or_404(User, username=request.user)
    context = {'user': user}
    return render(request, 'registration/profile.html', context)

@login_required(login_url='login')
def profileEditPassword(request):
    """Changing password on the profile page\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Redirect profile page
    """
    if request.user.has_usable_password() == False:
        messages.warning(request, 'You are connected with a third party system and cannot modify your information from this page.')
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            sweetify.success(request, 'Your password has been updated.', button='Ok', timer=5000)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    context = {"form": form}
    return render(request, 'registration/profile.html', context)

@login_required(login_url='login')
def profileEditInformation(request):
    """Changing basic information on the profile page\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Redirect profile page
    """
    if request.user.has_usable_password() == False:
        messages.warning(request, 'You are connected with a third party system and cannot modify your information from this page.')
    if request.method == 'POST':
        userForm = UserForm(request.POST, instance=request.user)
        profileForm = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            sweetify.success(request, 'Your information has been updated.', button='Ok', timer=5000)
            return redirect('profile')
    else:
        userForm = UserForm(instance=request.user)
        profileForm = ProfileForm(instance=request.user.profile)
    context = {'userForm': userForm, 'profileForm': profileForm}
    return render(request, 'registration/profile.html', context)

def home(request):
    """Displaying profile page\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Rendering home page
    """
    try:
        news = Post.objects.latest('id')
        trends = Post.objects.order_by('-id')[1:4]
        context = {'news': news, 'trends': trends}
    except:
        news = None
        trends = None
        context = {'news': news, 'trends': trends}
    return render(request, 'index.html', context)

def game(request):
    """Displaying profile page\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Rendering game page
    """
    context = {}
    return render(request, 'game.html', context)

@login_required(login_url='login')
def alpha(request):
    """Registration at ALPHA
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Rendering Alpha page
    """
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            obj, created = Game.objects.update_or_create(user=request.user)
            if created:
                obj.alpha = True
                obj.edit()
                sweetify.success(request, 'You are now registered for the Alpha.', button='Ok', timer=5000)
            else:
                obj.user = request.user
                obj.alpha = True
                obj.publish()
                sweetify.success(request, 'You are now registered for the Alpha.', button='Ok', timer=5000)
    else:
        form = GameForm()
    try:
        x = Game.objects.get(user=request.user)
        x = x.alpha
    except:
        x = False
    context = {'alpha': x}
    return render(request, 'alpha.html', context)

@login_required(login_url='login')
def beta(request):
    """Registration at BETA
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Rendering Beta page
    """
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            obj, created = Game.objects.update_or_create(user=request.user)
            if created:
                obj.beta = True
                obj.edit()
                sweetify.success(request, 'You are now registered for the Beta.', button='Ok', timer=5000)
            else:
                obj.user = request.user
                obj.beta = True
                obj.publish()
                sweetify.success(request, 'You are now registered for the Beta.', button='Ok', timer=5000)
    else:
        form = GameForm()
    try:
        x = Game.objects.get(user=request.user)
        x = x.beta
    except:
        x = False
    context = {'beta': x}
    return render(request, 'beta.html', context)

def news(request):
    """Recovery and management of posts\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Redirect to news page
    """
    posts = Post.objects.order_by('-created_date', '-last_edit')
    commonTags = Post.tags.most_common()[:4]
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.title = form.cleaned_data["title"]
            newpost.description = form.cleaned_data["description"]
            newpost.slug = slugify(newpost.title)
            try:
                newpost.publish()
                form.save_m2m()
                sweetify.success(request, 'Your post n°{0} has been uploaded.'.format(newpost.id), button='Ok', timer=5000)
                return redirect('news/post/{0}/'.format(newpost.id))
            except:
                sweetify.warning(request, 'A post with this title: {0} already exists.'.format(newpost.title), button='Ok', timer=5000)
    else:
        form = PostForm()
    context = {'posts': posts, 'commonTags': commonTags, 'form': form}
    return render(request, 'news.html', context)

def specificNews(request, id):
    """Recovering a specific news by its ID\n\n
    :param [request]: Receives an HttpRequest
    :param [id]: Receives Id linked to a post
    :type [request]: HttpRequest
    :type [id]: Integer
    :return: Redirect to news page
    """
    post = get_object_or_404(Post, id=id)
    context = {'post': post}
    return render(request, 'detail.html', context)

def tagged(request, id):
    """Recovery of a specific news by its Tag\n\n
    :param [request]: Receives an HttpRequest
    :param [id]: Receives id linked to a post
    :type [request]: HttpRequest
    :type [id]: Integer
    :return: Redirect to news page
    """
    tag = get_object_or_404(Tag, id=id)
    posts = Post.objects.filter(tags=tag)
    context = {'tag': tag, 'posts': posts}
    return render(request, 'news.html', context)

def contact(request):
    """Management of the contact form\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Redirect to contact page
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message'] + str(' of {0}'.format(name))
            try:
                send_mail(subject, message, from_email, ['tristan.mesurolle@epitech.eu'])
                sweetify.success(request, 'The mail has been sent successfully.', button='Ok', timer=5000)
            except BadHeaderError:
                sweetify.error(request, 'Invalid header found.', button='Ok', timer=5000)
            return redirect('contact')
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'contact.html', context)

def newsletter(request):
    """Newsletter subscription management\n\n
    :param [request]: Receives an HttpRequest
    :type [request]: HttpRequest
    :return: Redirect to newsletter page
    """
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            obj, created = Newsletter.objects.update_or_create(email=email)
            if created:
                obj.registered = True
                obj.edit()
                sweetify.success(request, 'You are now registered for the Newsletter.', button='Ok', timer=5000)
            else:
                obj.email = email
                obj.registered = True
                obj.publish()
                sweetify.success(request, 'You are now registered for the Newsletter.', button='Ok', timer=5000)
    else:
        form = NewsletterForm()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
