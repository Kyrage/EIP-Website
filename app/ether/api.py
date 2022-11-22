
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
        UserFriends.objects.create(user=instance)
        UserSkills.object.create(user=instance, _id=0, _parentId=2, name='FireTarget', level=1, equipped=0)
        UserSkills.object.create(user=instance, _id=1, _parentId=3, name='IceProjectile', level=1, equipped=0)

# --> FILTER
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

# <-- END FILTER
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
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset

# ------------- #

class UserDataSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)

    class Meta:
        model = UserData
        exclude = ('url', 'user')
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    def create(self, validated_data):
        try:
            obj = get_object_or_404(UserData, user=self.context.get("request").user, name=validated_data['name'])
            try:
                if validated_data['level']:
                    obj.level = validated_data['level']
            except:
                pass
            try:
                if validated_data['skinId']:
                    obj.skinId = validated_data['skinId']
            except:
                pass
            try:
                if validated_data['crystal']:
                    obj.crystal = validated_data['crystal']
            except:
                pass
            try:
                if validated_data['cash']:
                    obj.cash = validated_data['cash']
            except:
                pass
            try:
                if validated_data['mentoring']:
                    obj.mentoring = validated_data['mentoring']
            except:
                pass
            try:
                if validated_data['passif']:
                    obj.passif = validated_data['passif']
            except:
                pass
            try:
                if validated_data['textureSlot']:
                    obj.textureSlot = validated_data['textureSlot']
            except:
                pass
            try:
                if validated_data['maxTextureSlot']:
                    obj.maxTextureSlot = validated_data['maxTextureSlot']
            except:
                pass
            try:
                if validated_data['hasDoneTutorial']:
                    obj.hasDoneTutorial = validated_data['hasDoneTutorial']
            except:
                pass
            obj.edit()
            return (obj)
        except:
            if UserData.objects.filter(user=self.context.get("request").user).exists():
                return UserData.objects.filter(user=self.context.get("request").user)
            else:
                user = super(UserDataSerializer, self).create(validated_data)
                user.user = self.context.get("request").user
                user.name = self.context.get("request").user.username
                user.save()
                return (user)

class UserDataViewSet(viewsets.ModelViewSet):
    serializer_class = UserDataSerializer

    def get_queryset(self):
        user = self.request.user
        return UserData.objects.filter(user=user)

# ------------- #

class UserSkillsSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    class Meta:
        model = UserSkills
        exclude = ('url', 'user')
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    def create(self, validated_data):
        try:
            obj = get_object_or_404(UserSkills, user=self.context.get("request").user, name=validated_data['name'])
            obj.level = validated_data['level']
            obj.equipped = validated_data['equipped']
            obj.edit()
            return obj
        except:
            user = super(UserSkillsSerializer, self).create(validated_data)
            user.user = self.context.get("request").user
            user.save()
            return user

class UserSkillsViewSet(viewsets.ModelViewSet):
    serializer_class = UserSkillsSerializer

    def get_queryset(self):
        user = self.request.user
        return UserSkills.objects.filter(user=user)

# ------------- #

class UserInventorySerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    class Meta:
        model = UserInventory
        exclude = ('url', 'user')
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    def create(self, validated_data):
        try:
            obj = get_object_or_404(UserInventory, user=self.context.get("request").user, _id=validated_data['_id'])
            obj.quantity = validated_data['quantity']
            obj.edit()
            return obj
        except:
            user = super(UserInventorySerializer, self).create(validated_data)
            user.user = self.context.get("request").user
            user.save()
            return user

class UserInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = UserInventorySerializer

    def get_queryset(self):
        user = self.request.user
        return UserInventory.objects.filter(user=user)

# ------------- #

class UserFriendsSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    user_username = serializers.SerializerMethodField()
    friends_username = serializers.SerializerMethodField()
    all_users = serializers.SerializerMethodField()


    def get_user_username(self, obj):
        return self.context.get("request").user.username

    def get_friends_username(self, obj):
        user = self.context.get("request").user
        friend = UserFriends.objects.all().filter(user=user).order_by().values('friends__username')
        friend.exclude(friends__username=user.username)
        data = [obj['friends__username'] for obj in friend]
        return data

    def get_all_users(self, obj):
        return User.objects.all().values('username', 'id')

    class Meta:
        model = UserFriends
        fields = ['user_username', 'friends', 'friends_username', 'all_users']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    def create(self, validated_data):
        try:
            obj = get_object_or_404(UserFriends, user=self.context.get("request").user)
            if validated_data['friends']:
                for x in validated_data['friends']:
                    if x in obj.friends.all():
                        obj.remove_friend(User.objects.get(username=x))
                    else:
                        obj.add_friend(User.objects.get(username=x))
            obj.edit()
            return obj
        except:
            user = self.context.get("request").user
            if UserFriends.objects.filter(user=user).exists():
                return UserFriends.objects.filter(user=user)
            else:
                user = super(UserFriendsSerializer, self).create(validated_data)
                user.user = user
                user.save()
                return user

class UserFriendsViewSet(viewsets.ModelViewSet):
    serializer_class = UserFriendsSerializer

    def get_queryset(self):
        user = self.request.user
        return UserFriends.objects.filter(user=user).order_by()

# ------------- #

# class UserGuildSerializer(serializers.HyperlinkedModelSerializer):
#     permission_classes = (IsAuthenticated,)
#     class Meta:
#         model = UserGuild
#         fields = ['user', 'name']
#         read_only_fields = ['is_staff', 'is_superuser', 'user']

#     def create(self, validated_data):
#         try:
#             obj = get_object_or_404(UserGuild, user=self.context.get("request").user)
#             obj.name = validated_data['name']
#             obj.save()
#             return (obj)
#         except:
#             user = super(UserGuildSerializer, self).create(validated_data)
#             user.user = self.context.get("request").user
#             user.save()
#             return (user)

# class UserGuildViewSet(viewsets.ModelViewSet):
#     #queryset = UserGuild.objects.all()
#     serializer_class = UserGuildSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return UserGuild.objects.all().filter(user=user)

# class UserMatchmakingSerializer(serializers.HyperlinkedModelSerializer):
#     permission_classes = (IsAuthenticated,)
#     enemy = serializers.SerializerMethodField()
#     class Meta:
#         model = UserMatchmaking
#         fields = ['url', 'user', 'enemy']
#         read_only_fields = ['is_staff', 'is_superuser', 'user']

#     def create(self, validated_data):
#         try:
#             user = get_object_or_404(UserMatchmaking, user=self.context.get("request").user)
#             return (user)
#         except:
#             user = super(UserMatchmakingSerializer, self).create(validated_data)
#             user.user = self.context.get("request").user
#             user.save()
#             return (user)

#     def get_enemy(self, obj):
#             level = get_object_or_404(UserData, user=self.context.get("request").user).level
#             enemy = UserMatchmaking.objects.all().filter(user__userdata__level=level).values('user', 'user__username')
#             enemy = enemy.exclude(user__username=obj)
#             fighter = enemy.order_by('?').first()
#             try:
#                 return ("http://localhost/api/users/" + str(fighter['user']) + "/")
#             except:
#                 return None

# class UserMatchmakingViewSet(viewsets.ModelViewSet):
#     queryset = UserMatchmaking.objects.all()
#     serializer_class = UserMatchmakingSerializer

class UserTextureSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    class Meta:
        model = UserTexture
        exclude = ('url', 'user')
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    @csrf_exempt
    def create(self, validated_data):
        try:
            obj = UserTexture.objects.get(user=self.context.get("request").user, id=validated_data['id'])
            obj.texture = validated_data['texture']
            obj.edit()
            return (obj)
        except:
            user = super(UserTextureSerializer, self).create({ 'texture': validated_data['texture'] })
            user.user = self.context.get("request").user
            user.save()
            return (user)

class UserTextureViewSet(viewsets.ModelViewSet):
    queryset = UserTexture.objects.all()
    serializer_class = UserTextureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilterTexture

class CommutaryShopSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    class Meta:
        model = Shop
        fields = ['user', 'id', 'data']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    @csrf_exempt
    def create(self, validated_data):
        if Shop.objects.filter(user=self.context.get("request").user).exists():
            obj = Shop.objects.get(user=self.context.get("request").user)
            obj.data = validated_data['data']
            obj.save()
            return (obj)
        else:
            user = super(CommutaryShopSerializer, self).create(validated_data)
            user.user = self.context.get("request").user
            user.save()
            return (user)

class CommutaryViewSet(viewsets.ModelViewSet):
    serializer_class = CommutaryShopSerializer

    def get_queryset(self):
        queryset = Shop.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(user__username=username)
        return queryset

class CommutaryTextureShopSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    class Meta:
        model = ShopTexture
        fields = ['seller', 'id', 'texture', 'price']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    @csrf_exempt
    def create(self, validated_data):
        try:
            print(validated_data['id'])
            if ShopTexture.objects.filter(id=validated_data['id']).exists():
                obj = ShopTexture.objects.get(id=validated_data['id'])
                if validated_data['price'] == 0:
                    obj.delete()
                else:
                    obj.price = validated_data['price']
                    obj.save()
                return (obj)
            else:
                user = super(CommutaryTextureShopSerializer, self).create(validated_data)
                user.seller = self.context.get("request").user
                user.save()
                return (user)
        except:
            user = super(CommutaryTextureShopSerializer, self).create(validated_data)
            user.seller = self.context.get("request").user
            user.save()
            return (user)

class CommutaryTextureViewSet(viewsets.ModelViewSet):
    serializer_class = CommutaryTextureShopSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = ShopTexture.objects.all()
        return queryset.exclude(seller=user)

class UserDungeonsSerializer(serializers.HyperlinkedModelSerializer):
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    class Meta:
        model = UserDungeons
        fields = ['user', 'id', 'data']
        read_only_fields = ['is_staff', 'is_superuser', 'user']

    @csrf_exempt
    def create(self, validated_data):
        if UserDungeons.objects.filter(user=self.context.get("request").user).exists():
            obj = UserDungeons.objects.get(user=self.context.get("request").user)
            obj.data = validated_data['data']
            obj.save()
            return (obj)
        else:
            user = super(UserDungeonsSerializer, self).create(validated_data)
            user.user = self.context.get("request").user
            user.save()
            return (user)

class UserDungeonsViewSet(viewsets.ModelViewSet):
    serializer_class = UserDungeonsSerializer

    def get_queryset(self):
        queryset = UserDungeons.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(user__username=username)
        return queryset

class DeleteUserDungeonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class DeleteUserDungeonsViewSet(viewsets.ModelViewSet):
    queryset = UserDungeons.objects.all()
    serializer_class = DeleteUserDungeonsSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['delete', ]

    def destroy(self, request, pk=None, *args, **kwargs):
        return super(DeleteUserDungeonsViewSet, self).destroy(request, pk, *args, **kwargs)