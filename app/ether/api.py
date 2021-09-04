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
        fields = ['url', 'username', 'password', 'first_name', 'last_name', 'email']
        read_only_fields = ['is_staff', 'is_superuser']
        write_only_fields = ['password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return (instance)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return (instance)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserSkillsSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    class Meta:
        model = UserSkills
        fields = ['url', 'author', 'cap_1', 'cap_2', 'cap_3', 'cap_4']
        read_only_fields = ['is_staff', 'is_superuser']

class UserSkillsViewSet(viewsets.ModelViewSet):
    queryset = UserSkills.objects.all()
    serializer_class = UserSkillsSerializer

class UserPositionsSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    class Meta:
        model = UserPositions
        fields = ['url', 'author', 'x', 'y', 'z']
        read_only_fields = ['is_staff', 'is_superuser']

class UserPositionsViewSet(viewsets.ModelViewSet):
    queryset = UserPositions.objects.all()
    serializer_class = UserPositionsSerializer

class UserInventorySerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    class Meta:
        model = UserInventory
        fields = ['url', 'author', 'item', 'number']
        read_only_fields = ['is_staff', 'is_superuser']

class UserInventoryViewSet(viewsets.ModelViewSet):
    queryset = UserInventory.objects.all()
    serializer_class = UserInventorySerializer

class UserFriendsSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    class Meta:
        model = UserFriends
        fields = ['url', 'author', 'name']
        read_only_fields = ['is_staff', 'is_superuser']

class UserFriendsViewSet(viewsets.ModelViewSet):
    queryset = UserFriends.objects.all()
    serializer_class = UserFriendsSerializer

class UserGuildSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    class Meta:
        model = UserGuild
        fields = ['url', 'author', 'name']
        read_only_fields = ['is_staff', 'is_superuser']

class UserGuildViewSet(viewsets.ModelViewSet):
    queryset = UserGuild.objects.all()
    serializer_class = UserGuildSerializer
