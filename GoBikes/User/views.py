from plistlib import UID
from tracemalloc import start
from datetime import datetime
from datetime import timedelta
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_list_or_404, render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from .models import StatisticsMgr, Target, Location, Trip, Post, BicycleStand, DistAPI, DestAPI, LoopAPI, LeaderboardMgr, StatisticsMgr, GPSPings
from .serializers import TargetSerializer, UserCreateSerializer, TargetSerializer, LocationSerializer, TripSerializer, PostSerializer, BicycleStandSerializer, DistAPISerializer, DestAPISerializer, LoopAPISerializer, GPSPingsSerializer
# For the User Model
from django.contrib.auth import get_user_model
User = get_user_model()


class UserView(viewsets.ModelViewSet):
    #permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    @action(methods=['post'], detail=False)
    def getUserByID(self, request):
        response = User.objects.getUser(
            ID=int(request.data["UID"]))
        return Response(response)
    # Check Permissions


# class UserActivationView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, uid, token):
#         protocol = 'https://' if request.is_secure() else 'http://'
#         web_url = protocol + request.get_host()
#         post_url = web_url + "/auth/users/activation/"
#         post_data = {'uid': uid, 'token': token}
#         result = requests.post(post_url, data=post_data)
#         content = result.text
#         return Response(content)

# User Activation Email was removed


class TargetView(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    @action(methods=['post'], detail=False)
    def target(self, request):
        response = Target.TargetMgr.getTarget(
            UID=int(request.data["UID"]))
        return Response(response)


# class LocationView(viewsets.ModelViewSet):
#     queryset = Location.objects.all()
#     serializer_class = LocationSerializer

class GPSPingsView(viewsets.ModelViewSet):
    queryset = GPSPings.objects.all()
    serializer_class = GPSPingsSerializer

    @ action(methods=['post'], detail=False)
    def add(self, request):
        temp = {
            "UID": 1,
            "startLat": 0,
            "startLng": 0,
            "endLat": 0,
            "endLng": 0,
            "startTime": "2022-04-03T12:34:56.000000Z",
            "endTime": "2022-04-03T12:40:56.000000Z",
            "date": "2013-01-29",
            "distance": 0,
            "calories": 0,
        }
        result = TripView.save(temp)
        GPSPingsView.save(request)

    # queryset = request.data
    # print(queryset)
    # dat = []
    # serializer = GPSPingsSerializer(data=queryset["pings"],many=True)
    # print(serializer)
    # if serializer.is_valid():
    #     dat.append(serializer)
    #     TripView.create({"UID" : int(dat[0]["UID"]),
    #                 "startLat" :dat[0]["latitude"],
    #                 "startLng" :dat[0]["longitude"],
    #                 "endLat" :dat[-1]["latitude"],
    #                 "endLng" :dat[-1]["longitude"],
    #                 "startTime" : dat[0]["timestamp"],
    #                 "endTime" : dat[-1]["timestamp"],
    #                 "distance" : request["distance"],
    #                 "calories" : request["calories"]})
    #     return Response(serializer.data)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripView(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    @ action(methods=['post'], detail=False)
    def startTrip(self, request):
        temp = {"UID": request.data["UID"],
                "startLat": request.data["startLat"],
                "startLng": request.data["startLng"],
                "startTime":  request.data["startTime"],
                "date": request.data["date"],
                "distance": 0,
                "calories":  0}
        serializer = TripSerializer(data=temp)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data["id"])
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @ action(methods=['post'], detail=False)
    def endTrip(self, request):
        tid = request.data["TID"]
        num = GPSPings.objects.filter(TID=tid).values(
            "TID").annotate(distance=Count("TID"))
        print(num)
        num = num[0]["distance"]
        Trip.objects.filter(pk=tid).update(
            distance=num*30, calories=num*num*30*30/10)
        return Response("Succesful")

    @ action(methods=['post'], detail=False)
    def Day(self, request):
        response = LeaderboardMgr.displayDailyLeaderboard(
            UID=int(request.data["UID"]))
        return Response(response)

    @ action(methods=['post'], detail=False)
    def Week(self, request):
        response = LeaderboardMgr.displayWeeklyLeaderboard(
            UID=int(request.data["UID"]))
        return Response(response)

    @ action(methods=['post'], detail=False)
    def Month(self, request):
        response = LeaderboardMgr.displayMonthlyLeaderboard(
            UID=int(request.data["UID"]))
        return Response(response)

    @ action(methods=['post'], detail=False)
    def DayCal(self, request):
        response = LeaderboardMgr.displayDailyCalLeaderboard(
            UID=int(request.data["UID"]))
        return Response(response)

    @ action(methods=['post'], detail=False)
    def WeekCal(self, request):
        response = LeaderboardMgr.displayWeeklyCalLeaderboard(
            UID=int(request.data["UID"]))
        return Response(response)

    @ action(methods=['post'], detail=False)
    def MonthCal(self, request):
        response = LeaderboardMgr.displayMonthlyCalLeaderboard(
            UID=int(request.data["UID"]))
        return Response(response)

    @ action(methods=['post'], detail=False)
    def UserDay(self, request):
        S = StatisticsMgr()
        response = S.getStatisticsDaily(UID=int(request.data["UID"]))
        return Response(response)

    @ action(methods=['post'], detail=False)
    def UserMonth(self, request):
        S = StatisticsMgr()
        response = S.getStatisticsMonthly(UID=int(request.data["UID"]))
        return Response(response)

    @ action(methods=['post'], detail=False)
    def UserWeek(self, request):
        S = StatisticsMgr()
        response = S.getStatisticsWeekly(UID=int(request.data["UID"]))
        return Response(response)


# class PostView(viewsets.ModelViewSet):
#     queryset = Post.objects.order_by("-timestamp")
#     serializer_class = PostSerializer

#     @ action(methods=["get"], detail=False)
#     def getPosts(self, requests):
#         result = Post.PostMgr.getLatestPost()
#         user = []
#         for i in result:
#             user.append(User.UserMgr.getUser(i["UserID_id"])[0])

#         return Response({"result": result, "user": user})

class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.order_by("-timestamp")
    serializer_class = PostSerializer

    @ action(methods=["get"], detail=False)
    def getPosts(self, requests):
        result = Post.PostMgr.getLatestPost()
        # user = []
        resp = []
        for i in result:
            resp.append([i, User.objects.getUser(i["UserID_id"])[0]])
            # user.append(User.objects.getUser(i["UserID_id"])[0])

        return Response({"result": resp})

# class BicycleStandView(viewsets.ModelViewSet):
#     queryset = BicycleStand.objects.all()
#     serializer_class = BicycleStandSerializer


class DistAPIView(viewsets.ModelViewSet):
    queryset = DistAPI.objects.all()
    serializer_class = DistAPISerializer

    @ action(methods=["post"], detail=False)
    def getPings(self, request):
        serializer = DistAPISerializer(data=request.data)
        if serializer.is_valid():
            startLoc = {
                "latitude": serializer.data["startLat"], "longitude": serializer.data["startLng"]}
            startStand = BicycleStand.BicycleMgr.findNearestStand(startLoc)
            endLoc = {
                "latitude": serializer.data["endLat"], "longitude": serializer.data["endLng"]}
            endStand = BicycleStand.BicycleMgr.findNearestStand(endLoc)
            pings = Trip.TripMgr.makeTripB(
                startLoc, endLoc, startStand, endStand)
            return Response(pings)
        else:
            return Response(serializer.errors)


class DestAPIView(viewsets.ModelViewSet):
    queryset = DestAPI.objects.all()
    serializer_class = DestAPISerializer

    @ action(methods=["post"], detail=False)
    def getPings(self, request):
        serializer = DestAPISerializer(data=request.data)
        if serializer.is_valid():
            start = {
                "latitude": serializer.data["lat"], "longitude": serializer.data["lng"]}
            start_ = {"lat": serializer.data["lat"],
                      "lng": serializer.data["lng"]}
            i = serializer.data["visited"]
            startStand = BicycleStand.BicycleMgr.findNearestStand(start)
            startStand_ = {
                "lat": startStand["latitude"], "lng": startStand["longitude"]}
            pings = Trip.TripMgr.makeTripC(start_, i, startStand_)
            return Response(pings)
        else:
            return Response(serializer.errors)


class LoopAPIView(viewsets.ModelViewSet):
    queryset = LoopAPI.objects.all()
    serializer_class = LoopAPISerializer

    @ action(methods=["post"], detail=False)
    def getPings(self, request):
        serializer = LoopAPISerializer(data=request.data)
        if serializer.is_valid():
            start = {
                "latitude": serializer.data["lat"], "longitude": serializer.data["lng"]}
            start_ = {"lat": serializer.data["lat"],
                      "lng": serializer.data["lng"]}
            startStand = BicycleStand.BicycleMgr.findNearestStand(start)
            startStand_ = {
                "lat": startStand["latitude"], "lng": startStand["longitude"]}
            pings = Trip.TripMgr.makeTripD(
                start_, startStand_, serializer.data["dist"])
            return Response(pings)
        else:
            return Response(serializer.errors)
