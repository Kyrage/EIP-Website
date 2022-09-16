from email.mime import base
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from rest_framework import routers
from . import views
from . import api

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    # Login/Register with django
    path('account/register/', views.register, name='register'),
    # Activation link
    path('activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activateAccount, name='activateAccount'),
    # Profile connected user
    path('account/profile/', views.profile, name='profile'),
    path('account/profile/edit/password', views.profileEditPassword, name='profileEditPassword'),
    path('account/profile/edit/information', views.profileEditInformation, name='profileEditInformation'),
    # Game page
    path('ether', views.game, name='game'),
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
    # Randomizer
    path('randomizer', views.randomizer, name='randomizer'),
]

router = routers.DefaultRouter()
router.register('users', api.UserViewSet)
router.register('users_data', api.UserDataViewSet, basename='users_data')
router.register('users_skills', api.UserSkillsViewSet, basename='users_skills')
router.register('users_inventory', api.UserInventoryViewSet, basename='users_inventory')
router.register('users_friends', api.UserFriendsViewSet, basename='users_friends')
router.register('users_guild', api.UserGuildViewSet, basename='users_guild')
#router.register('game/users_matchmaking', api.UserMatchmakingViewSet)
router.register('game/users_texture', api.UserTextureViewSet)
router.register('shop/textures', api.CommutaryTextureViewSet, basename='shop_textures')

urlpatterns += [
    path('api/', include(router.urls)),
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/login-auth/', include('rest_framework.urls', namespace='rest_framework'))
]