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
        UserData.objects.create(user=instance)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    class Meta:
        model = User
        fields = '__all__'
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

class UserDataSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    user = serializers.CurrentUserDefault()

    class Meta:
        model = UserData
        fields = ['url', 'user', 'level', 'gold', 'gem']
        read_only_fields = ['is_staff', 'is_superuser']

class UserDataViewSet(viewsets.ModelViewSet):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer

class UserSkillsSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    user = serializers.CurrentUserDefault()
    class Meta:
        model = UserSkills
        fields = ['url', 'user', 'cap_1', 'cap_2', 'cap_3', 'cap_4']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

class UserSkillsViewSet(viewsets.ModelViewSet):
    queryset = UserSkills.objects.all()
    serializer_class = UserSkillsSerializer

class UserPositionsSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    user = serializers.CurrentUserDefault()
    class Meta:
        model = UserPositions
        fields = ['url', 'user', 'map', 'x', 'y', 'z']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

class UserPositionsViewSet(viewsets.ModelViewSet):
    queryset = UserPositions.objects.all()
    serializer_class = UserPositionsSerializer

class UserInventorySerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    user = serializers.CurrentUserDefault()
    class Meta:
        model = UserInventory
        fields = ['url', 'user', 'item', 'number']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

class UserInventoryViewSet(viewsets.ModelViewSet):
    queryset = UserInventory.objects.all()
    serializer_class = UserInventorySerializer

class UserFriendsSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    user = serializers.CurrentUserDefault()
    class Meta:
        model = UserFriends
        fields = ['url', 'user', 'name']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

class UserFriendsViewSet(viewsets.ModelViewSet):
    queryset = UserFriends.objects.all()
    serializer_class = UserFriendsSerializer

class UserGuildSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    user = serializers.CurrentUserDefault()
    class Meta:
        model = UserGuild
        fields = ['url', 'user', 'name']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

class UserGuildViewSet(viewsets.ModelViewSet):
    queryset = UserGuild.objects.all()
    serializer_class = UserGuildSerializer
