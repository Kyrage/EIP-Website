"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from ether.views import resetPassword
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('gestion/', admin.site.urls),
    path('', include('ether.urls')),
    path('auth/', include('djoser.urls')),
    path('account/login/', views.LoginView.as_view(), name='login'),
    path('account/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('account/passwordReset/', resetPassword, name='resetPassword'),
    path('account/passwordReset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/resetPassword.html"), name='password_reset_confirm'),
    path('account/passwordReset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/resetComplete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error handling
handler401 = 'ether.views.handler401'
handler404 = 'ether.views.handler404'
handler500 = 'ether.views.handler500'
