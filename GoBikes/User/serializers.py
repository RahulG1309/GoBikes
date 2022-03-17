from rest_framework import serializers
from .models import User, Location, Trip

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'