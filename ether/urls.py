from django.urls import path
from . import views


urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    path('ether', views.games, name='games'),
    path('ether/alpha', views.alpha, name='alpha'),
    path('ether/beta', views.beta, name='beta'),
    path('news', views.news, name='news'),
    path('contact', views.contact, name='contact'),
]