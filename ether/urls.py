from django.urls import path
from . import views


urlpatterns = [

    # Login/Register with django
    path('account/register/', views.register, name='register'),

    # Activation account link
    path('activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),

    # Profile connected user
    path('account/profile/', views.profile, name='profile'),
    
    # Home page
    path('', views.home, name='home'),

    # Games page
    path('ether', views.games, name='games'),
    path('ether/alpha', views.alpha, name='alpha'),
    path('ether/beta', views.beta, name='beta'),

    # Blog page
    path('news', views.news, name='news'),

    # Contact page
    path('contact', views.contact, name='contact'),
]