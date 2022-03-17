from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Location, Trip
from .serializers import UserSerializer, LoactionSerializer, TripSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LocationView(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LoactionSerializer

class TripView(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer