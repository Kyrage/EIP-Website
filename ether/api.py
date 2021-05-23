from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import serializers, viewsets
from django.contrib.auth.models import User
from .views import *

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def initToken(sender, instance=None, created=False, **kwargs):
    """
    Creation d'un Token a la creation d'un utilisateur
    """
    if created:
        Token.objects.create(user=instance)
class UserSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer