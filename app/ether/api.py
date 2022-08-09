
from django.http import HttpResponse
from rest_framework.fields import CurrentUserDefault
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import serializers, viewsets
from django.db.models.aggregates import Count
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend, CharFilter, FilterSet
from rest_framework import filters
from rest_framework.request import Request

from rest_framework.parsers import *
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from random import randint
from .views import *

import json

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def initToken(sender, instance=None, created=False, **kwargs):
    """
    Creation d'un Token a la creation d'un utilisateur
    """
    if created:
        Token.objects.create(user=instance)
        UserData.objects.create(user=instance)

class UserFilterData(FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='iexact')

    class Meta:
        fields = ('username',)
        model = UserData

class UserFilterTexture(FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='iexact')

    class Meta:
        fields = ('username',)
        model = UserTexture

class ShopFilterTexture(FilterSet):
    username = CharFilter(field_name='seller__username', lookup_expr='iexact')

    class Meta:
        fields = ('username',)
        model = ShopTexture

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

    class Meta:
        model = UserData
        fields = ['user', 'name', 'level', 'crystal', 'cash', 'mentoring', 'textureSlot', 'maxTextureSlot', 'hasDoneTutorial']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    def create(self, validated_data):
        try:
            obj = get_object_or_404(UserData, user=self.context.get("request").user)
            obj.name = self.context.get("request").user.username
            obj.level = validated_data['level']
            obj.crystal = validated_data['crystal']
            obj.cash = validated_data['cash']
            obj.mentoring = validated_data['mentoring']
            obj.textureSlot = validated_data['textureSlot']
            obj.maxTextureSlot = validated_data['maxTextureSlot']
            obj.hasDoneTutorial = validated_data['hasDoneTutorial']
            obj.save()
            return (obj)
        except:
            user = super(UserDataSerializer, self).create(validated_data)
            user.user = self.context.get("request").user
            user.name = self.context.get("request").user.username
            user.save()
            return (user)

class UserDataViewSet(viewsets.ModelViewSet):
    #queryset = UserData.objects.all()
    serializer_class = UserDataSerializer
    #filter_backends = [DjangoFilterBackend]
    #filterset_class = UserFilterData

    def get_queryset(self):
        user = self.request.user
        return UserData.objects.all().filter(user=user)

class UserSkillsSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    class Meta:
        model = UserSkills
        fields = ['_id', '_parentId', 'name', 'level', 'equipped']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    def create(self, validated_data):
        try:
            obj = get_object_or_404(UserSkills, user=self.context.get("request").user, name=validated_data['name'])
            obj.level = validated_data['level']
            obj.equipped = validated_data['equipped']
            obj.save()
            return (obj)
        except:
            user = super(UserSkillsSerializer, self).create(validated_data)
            user.user = self.context.get("request").user
            user.save()
            return (user)

class UserSkillsViewSet(viewsets.ModelViewSet):
    #queryset = UserSkills.objects.all()
    serializer_class = UserSkillsSerializer

    def get_queryset(self):
        user = self.request.user
        return UserSkills.objects.all().filter(user=user)

class UserInventorySerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    class Meta:
        model = UserInventory
        fields = ['_id', 'name', 'quantity', 'comment']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    def create(self, validated_data):
        try:
            obj = get_object_or_404(UserInventory, user=self.context.get("request").user, name=validated_data['name'])
            obj.quantity = validated_data['quantity']
            obj.save()
            return (obj)
        except:
            user = super(UserInventorySerializer, self).create(validated_data)
            user.user = self.context.get("request").user
            user.save()
            return (user)

class UserInventoryViewSet(viewsets.ModelViewSet):
    #queryset = UserInventory.objects.all()
    serializer_class = UserInventorySerializer

    def get_queryset(self):
        user = self.request.user
        return UserInventory.objects.all().filter(user=user)

class UserFriendsSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
      return obj.user.username
    class Meta:
        model = UserFriends
        fields = ['user', 'friends']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

class UserFriendsViewSet(viewsets.ModelViewSet):
    serializer_class = UserFriendsSerializer

    def get_queryset(self):
        user = self.request.user
        UserFriends.objects.get(user=user).add_friend(User.objects.get(username='adminTest'))
        return UserFriends.objects.all().filter(user=user)

class UserGuildSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    class Meta:
        model = UserGuild
        fields = ['url', 'user', 'name']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    def create(self, validated_data):
        try:
            obj = get_object_or_404(UserGuild, user=self.context.get("request").user)
            obj.name = validated_data['name']
            obj.save()
            return (obj)
        except:
            user = super(UserGuildSerializer, self).create(validated_data)
            user.user = self.context.get("request").user
            user.save()
            return (user)

class UserGuildViewSet(viewsets.ModelViewSet):
    queryset = UserGuild.objects.all()
    serializer_class = UserGuildSerializer

class UserMatchmakingSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    enemy = serializers.SerializerMethodField()
    class Meta:
        model = UserMatchmaking
        fields = ['url', 'user', 'enemy']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    def create(self, validated_data):
        try:
            user = get_object_or_404(UserMatchmaking, user=self.context.get("request").user)
            return (user)
        except:
            user = super(UserMatchmakingSerializer, self).create(validated_data)
            user.user = self.context.get("request").user
            user.save()
            return (user)

    def get_enemy(self, obj):
            level = get_object_or_404(UserData, user=self.context.get("request").user).level
            enemy = UserMatchmaking.objects.all().filter(user__userdata__level=level).values('user', 'user__username')
            enemy = enemy.exclude(user__username=obj)
            fighter = enemy.order_by('?').first()
            try:
                return ("http://localhost/api/users/" + str(fighter['user']) + "/")
            except:
                return None
            # if len(enemy) > 1:
            #     i = randint(0, len(enemy) - 1)
            #     UserMatchmaking.objects.filter(user__userdata__name__in=[obj, enemy[i]['user__username']]).delete()
            #     return ("http://localhost/api/users/" + str(enemy[i]['user']) + "/")
            # else:
            #     try:
            #         UserMatchmaking.objects.filter(user__userdata__name__in=[obj, enemy[0]['user__username']]).delete()
            #         return ("http://localhost/api/users/" + str(enemy[0]['user']) + "/")
            #     except:
            #         return (None)

class UserMatchmakingViewSet(viewsets.ModelViewSet):
    queryset = UserMatchmaking.objects.all()
    serializer_class = UserMatchmakingSerializer

class UserTextureSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    class Meta:
        model = UserTexture
        fields = ['id', 'texture']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    @csrf_exempt
    def create(self, validated_data):
        user = super(UserTextureSerializer, self).create(validated_data)
        user.user = self.context.get("request").user
        user.save()
        return (user)

class UserTextureViewSet(viewsets.ModelViewSet):
    queryset = UserTexture.objects.all()
    serializer_class = UserTextureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilterTexture

class CommutaryTextureShopSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    class Meta:
        model = ShopTexture
        fields = ['seller', 'id', 'texture', 'price']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    @csrf_exempt
    def create(self, validated_data):
        user = super(CommutaryTextureShopSerializer, self).create(validated_data)
        user.user = self.context.get("request").user
        user.save()
        return (user)

class CommutaryTextureViewSet(viewsets.ModelViewSet):
    #queryset = ShopTexture.objects.all()
    serializer_class = CommutaryTextureShopSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShopFilterTexture

    def get_queryset(self):
        user = self.request.user
        queryset = ShopTexture.objects.all()
        return queryset.exclude(seller=user)