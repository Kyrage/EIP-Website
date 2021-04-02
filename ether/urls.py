from django.urls import path
from . import views

urlpatterns = [
    # Login/Register with django
    path('account/register/', views.register, name='register'),

    # Activation link
    path('activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activateAccount, name='activateAccount'),

    # Profile connected user
    path('account/profile/', views.profile, name='profile'),
    path('account/profile/edit/password', views.profileEditPassword, name='profileEditPassword'),
    path('account/profile/edit/information', views.profileEditInformation, name='profileEditInformation'),
    
    # Home page
    path('', views.home, name='home'),

    # Games page
    path('ether', views.games, name='games'),
    path('ether/alpha', views.alpha, name='alpha'),
    path('ether/beta', views.beta, name='beta'),

    # Blog page
    path('news', views.news, name='news'),
    path('news/post/<id>/', views.specificNews, name="detail"),
    path('news/tag/<id>/', views.tagged, name="tagged"),

    # Contact page
    path('contact', views.contact, name='contact'),

    # Newsletter
    path('newsletter', views.newsletter, name='newsletter'),
]