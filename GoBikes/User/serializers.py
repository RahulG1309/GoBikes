from rest_framework import serializers
from .models import User, Target, Location, Trip, Post, BicycleStand, DistAPI, DestAPI, LoopAPI, GPSPings
# For Authentication
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


# class UserSerializer(UserSerializer):
#     class Meta(UserSerializer.Meta):
#         model = User
#         fields = '__all__'
# Is not required

class GPSPingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSPings
        fields = '__all__'

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'age',
                  'gender', 'hasBicycle', 'password')


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class BicycleStandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BicycleStand
        fields = '__all__'


class DistAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = DistAPI
        fields = '__all__'


class DestAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = DestAPI
        fields = '__all__'


class LoopAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = LoopAPI
        fields = '__all__'
