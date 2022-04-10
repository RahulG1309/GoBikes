import json
import requests
import googlemaps

from multiprocessing import Manager, managers
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from datetime import datetime
from datetime import timedelta
from django.db.models import Sum, Avg
from django.utils.translation import gettext_lazy as _


# def upload_to(self, fileName):
#     return 'user/{file}'.format(file=fileName)


class Location(models.Model):
    # has to be of format nn.nnnnnn
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    # has to be of format nn.nnnnnn
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

    def __str__(self):
        return (self.latitude, self.longitude)


class UserMgr(BaseUserManager):
    def create_user(self, email, name, age, gender, hasBicycle, password=None, **extra_arguments):
        if not email:
            raise ValueError('Users must enter email address')
        if not name:
            raise ValueError('Users must enter name')
        if not age:
            raise ValueError('Users must enter age')
        if not gender:
            raise ValueError('Users must enter gender')
        if not hasBicycle:
            raise ValueError('Users must enter hasBicycle')
        if not password:
            raise ValueError('Users must enter password')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, age=age,
                          gender=gender, hasBicycle=hasBicycle, **extra_arguments)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, age, gender, hasBicycle, password=None, **extra_arguments):
        if not email:
            raise ValueError('Users must enter email address')
        if not name:
            raise ValueError('Users must enter name')
        if not age:
            raise ValueError('Users must enter age')
        if not gender:
            raise ValueError('Users must enter gender')
        if not hasBicycle:
            raise ValueError('Users must enter hasBicycle')
        if not password:
            raise ValueError('Users must enter password')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, age=age,
                          gender=gender, hasBicycle=hasBicycle, **extra_arguments)

        user.set_password(password)
        user.save()

        return user

    def getUser(self, ID):
        return self.model.objects.filter(id=ID).values()


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    # gender = models.BooleanField(null=True, blank=True)
    # hasBicycle = models.BooleanField(null=True, blank=True, default=False)
    gender = models.CharField(max_length=1)  # M, F, T etc
    hasBicycle = models.CharField(max_length=1)  # Y, N etc
    is_active = models.BooleanField(default=True)
    # a admin user; non super-user
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    # Email & Password are required by default.
    REQUIRED_FIELDS = ['name', 'age']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     return self.staff

    # @property
    # def is_admin(self):
    #     "Is the user a admin member?"
    #     return self.admin

    objects = UserMgr()
    UserMgr = UserMgr()
    # Special, normal Manager() does not have create_user


class TargetMgr(models.Manager):
    def getTarget(self, UID):
        return self.model.objects.filter(timestamp__gte=datetime.now()-timedelta(weeks=1)).filter(UserID=UID).order_by("-timestamp")[:1].values()


class Target(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    totalDist = models.PositiveIntegerField(default=0)
    totalCal = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    # profilePhoto = models.ImageField(
    #     _("Image"), upload_to=upload_to, default="user/default.jpg")

    def __str__(self):
        return (self.UID, self.totalDist, self.totalCal)
    # Extension of User model, has targets

    objects = models.Manager()
    TargetMgr = TargetMgr()


class TripMgr(models.Manager):
    def userDaily(self, UID):
        querydist = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(days=1)).filter(UID=UID).values("UID").annotate(tot_dist=Sum("distance"))
        querycal = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(days=1)).filter(UID=UID).values("UID").annotate(tot_cal=Sum("calories"))
        avgdist = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(days=1)).filter(UID=UID).values("UID").annotate(avg_dist=Avg("distance"))
        avgcal = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(days=1)).filter(UID=UID).values("UID").annotate(avg_cal=Avg("calories"))
        return {"dist": querydist, "cal": querycal, "avgdist": avgdist, "avgcal": avgcal}

    def userWeekly(self, UID):
        querydist = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(weeks=1)).filter(UID=UID).values("UID").annotate(tot_dist=Sum("distance"))
        querycal = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(weeks=1)).filter(UID=UID).values("UID").annotate(tot_cal=Sum("calories"))
        avgdist = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(weeks=1)).filter(UID=UID).values("UID").annotate(avg_dist=Avg("distance"))
        avgcal = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(weeks=1)).filter(UID=UID).values("UID").annotate(avg_cal=Avg("calories"))
        return {"dist": querydist, "cal": querycal, "avgdist": avgdist, "avgcal": avgcal}

    def userMonthly(self, UID):
        querydist = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(weeks=4)).filter(UID=UID).values("UID").annotate(tot_dist=Sum("distance"))
        querycal = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(weeks=4)).filter(UID=UID).values("UID").annotate(tot_cal=Sum("calories"))
        avgdist = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(weeks=4)).filter(UID=UID).values("UID").annotate(avg_dist=Avg("distance"))
        avgcal = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(weeks=4)).filter(UID=UID).values("UID").annotate(avg_cal=Avg("calories"))
        return {"dist": querydist, "cal": querycal, "avgdist": avgdist, "avgcal": avgcal}

    def queryDataWeekly(self):
        querydist = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(weeks=1)).values("UID").annotate(tot_dist=Sum("distance")).order_by("-tot_dist")
        querycal = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(weeks=1)).values("UID").annotate(tot_cal=Sum("calories")).order_by("-tot_cal")
        return {"dist": querydist, "cal": querycal}

    def queryDataDaily(self):
        querydist = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(days=1)).values("UID").annotate(tot_dist=Sum("distance")).order_by("-tot_dist")
        querycal = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(days=1)).values("UID").annotate(tot_cal=Sum("calories")).order_by("-tot_cal")
        return {"dist": querydist, "cal": querycal}

    def queryDataMonthly(self):
        querydist = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(weeks=4)).values("UID").annotate(tot_dist=Sum("distance")).order_by("-tot_dist")
        querycal = self.model.objects.filter(startTime__gte=datetime.now(
        )-timedelta(weeks=4)).values("UID").annotate(tot_cal=Sum("calories")).order_by("-tot_cal")
        return {"dist": querydist, "cal": querycal}

    # def makeTripA(self,startLoc,endLoc,startStand,endStand):
    #     gmaps = googlemaps.Client(key='AIzaSyASF480RFv1t_BGvndNi8sO9EKZ2M7H0Vc')
    #     pings = []

    #     pings.append({"lat":startLoc["latitude"],"lng":startLoc["longitude"]})

    #     first = gmaps.directions(origin=startLoc, destination=startStand, mode="walking")[0]["legs"][0]["steps"]
    #     for i in first:
    #         pings.append(i["start_location"])

    #     second = gmaps.directions(origin=startStand, destination=endStand, mode="bicycling")[0]["legs"][0]["steps"]
    #     for i in second:
    #         pings.append(i["start_location"])

    #     third = gmaps.directions(origin=endStand, destination=endLoc, mode="walking")[0]["legs"][0]["steps"]
    #     for i in third:
    #         pings.append(i["start_location"])

    #     pings.append({"lat":endLoc["latitude"],"lng":endLoc["longitude"]})

    #     return pings

    def makeTripB(self, startLoc, endLoc, startStand, endStand):
        start = {"lat": startLoc["latitude"], "lng": startLoc["longitude"]}

        # first = gmaps.directions(origin=startLoc, destination=startStand, mode="walking")[0]["legs"][0]["steps"]
        # for i in first:
        #     polyline.append(i["polyline"]["points"])
        # else:
        #     pings.append(i["start_location"])

        first = MapAPI.MapAPIMgr.getLegPins(
            start, {"lat": startStand["latitude"], "lng": startStand["longitude"]}, "walking")

        # second = gmaps.directions(origin=startStand, destination=endStand, mode="bicycling")[0]["legs"][0]["steps"]
        # for i in second:
        #     polyline.append(i["polyline"]["points"])
        # else:
        #     pings.append(i["start_location"])

        second = MapAPI.MapAPIMgr.getLegPins({"lat": startStand["latitude"], "lng": startStand["longitude"]}, {
                                             "lat": endStand["latitude"], "lng": endStand["longitude"]}, "bicycling")

        # third = gmaps.directions(origin=endStand, destination=endLoc, mode="walking")[0]["legs"][0]["steps"]
        # for i in third:
        #     polyline.append(i["polyline"]["points"])

        third = MapAPI.MapAPIMgr.getLegPins({"lat": endStand["latitude"], "lng": endStand["longitude"]}, {
                                            "lat": endLoc["latitude"], "lng": endLoc["longitude"]}, "walking")

        plot = {"ping": (start, first["pings"], second["pings"], third["pings"]),
                "polyline": first["polyline"]+second["polyline"]+third["polyline"]}
        return plot

    def makeTripC(self, loc, iteration, stand):
        landmark = {}
        step = 500
        counter = 0
        while(landmark == {}):
            landmark = MapAPI.MapAPIMgr.findLandmark(
                loc, iteration, 2000+step*counter)
            counter = counter+1

        first = MapAPI.MapAPIMgr.getLegPins(loc, stand, "walking")
        second = MapAPI.MapAPIMgr.getLegPins(
            stand, landmark["loc"], "bicycling")

        plot = {"dest": landmark["name"], "ping": [
            loc, first["pings"], second["pings"]], "polyline": first["polyline"]+second["polyline"]}
        return plot

    def makeTripD(self, loc, stand, dist):
        # dist in metres, step in metres
        dist = dist/2
        counter = 0
        result = MapAPI.MapAPIMgr.findLandmarks(loc, abs(dist-500))
        tempName = set(result[0])
        var = []

        while(var == []):
            inResult = MapAPI.MapAPIMgr.findLandmarks(
                loc, dist+500*(counter+1))
            inName = inResult[0]
            inPing = inResult[1]
            var = list(set(inName) - tempName)
            counter = counter+1

        req = []
        for i in range(len(inName)):
            if(inName[i] == var[0]):
                req = inPing[i]

        first = MapAPI.MapAPIMgr.getLegPins(loc, stand, "walking")
        second = MapAPI.MapAPIMgr.getLegPins(stand, req, "bicycling")

        third = MapAPI.MapAPIMgr.getLegPinsAlt(req, stand, "bicycling")
        fourth = MapAPI.MapAPIMgr.getLegPins(stand, loc, "walking")

        plot = {"dest": var[0], "ping": [loc, first["pings"], second["pings"]],
                "polyline": first["polyline"]+second["polyline"]+third["polyline"]+fourth["polyline"]}
        return plot


class Trip(models.Model):
    UID = models.ForeignKey(User, on_delete=models.CASCADE)
    startLat = models.DecimalField(max_digits=10, decimal_places=6)
    startLng = models.DecimalField(max_digits=10, decimal_places=6)
    startTime = models.DateTimeField()
    date = models.DateField(auto_now_add=True)
    distance = models.DecimalField(max_digits=7, decimal_places=2)
    calories = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return str(self.UID)

    objects = models.Manager()
    TripMgr = TripMgr()


class GPSPings(models.Model):
    UID = models.ForeignKey(User, on_delete=models.CASCADE)
    TID = models.ForeignKey(Trip, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    latitude = models.DecimalField(max_digits=15, decimal_places=8)
    longitude = models.DecimalField(max_digits=15, decimal_places=8)


class StatisticsMgr():
    def getStatisticsDaily(self, UID):
        result = Trip.TripMgr.userDaily(UID)
        return result

    def getStatisticsWeekly(self, UID):
        result = Trip.TripMgr.userWeekly(UID)
        return result

    def getStatisticsMonthly(self, UID):
        result = Trip.TripMgr.userMonthly(UID)
        return result


class LeaderboardMgr(models.Model):
    def displayDailyLeaderboard(UID):
        day = Trip.TripMgr.queryDataDaily()
        rankings = []
        userRank = []
        counter = 1

        for i in day["dist"]:
            if counter > 20:
                break
            temp = User.UserMgr.getUser(i["UID"])[0]  # fix
            rankings.append(
                {"rank": counter, "user": temp["name"], "distance": i["tot_dist"]})
            counter = counter+1

        temp = User.UserMgr.getUser(UID)[0]  # fix
        rank = -1
        counter = 1
        dist = 0
        for j in day["dist"]:
            if j["UID"] == UID:
                rank = counter
                dist = j["tot_dist"]
                break
            counter = counter + 1

        userRank.append(
            {"rank": rank, "user": temp["name"], "distance": dist})

        return {"rankings": rankings, "userRank": userRank}

    def displayWeeklyLeaderboard(UID):
        day = Trip.TripMgr.queryDataWeekly()
        rankings = []
        userRank = []
        counter = 1

        for i in day["dist"]:
            if counter > 20:
                break
            temp = User.UserMgr.getUser(i["UID"])[0]  # fix
            rankings.append(
                {"rank": counter, "user": temp["name"], "distance": i["tot_dist"]})
            counter = counter+1

        temp = User.UserMgr.getUser(UID)[0]  # fix
        rank = -1
        counter = 1
        dist = 0
        for j in day["dist"]:
            if j['UID'] == UID:
                rank = counter
                dist = j["tot_dist"]
                break
            counter = counter + 1

        userRank.append(
            {"rank": rank, "user": temp["name"], "distance": dist})

        return {"rankings": rankings, "userRank": userRank}

    def displayMonthlyLeaderboard(UID):
        day = Trip.TripMgr.queryDataMonthly()
        rankings = []
        userRank = []
        counter = 1

        for i in day["dist"]:
            if counter > 20:
                break
            temp = User.UserMgr.getUser(i["UID"])[0]  # fix
            rankings.append(
                {"rank": counter, "user": temp["name"], "distance": i["tot_dist"]})
            counter = counter+1

        temp = User.UserMgr.getUser(UID)[0]  # fix
        rank = -1
        counter = 1
        dist = 0
        for j in day["dist"]:
            if j["UID"] == UID:
                rank = counter
                dist = j["tot_dist"]
                break
            counter = counter + 1

        userRank.append(
            {"rank": rank, "user": temp["name"], "distance": dist})

        return {"rankings": rankings, "userRank": userRank}

    def displayMonthlyCalLeaderboard(UID):
        day = Trip.TripMgr.queryDataMonthly()
        rankings = []
        userRank = []
        counter = 1

        for i in day["cal"]:
            if counter > 20:
                break
            temp = User.UserMgr.getUser(i["UID"])[0]  # fix
            rankings.append(
                {"rank": counter, "user": temp["name"], "distance": i["tot_cal"]})
            counter = counter+1

        temp = User.UserMgr.getUser(UID)[0]  # fix
        rank = -1
        counter = 1
        dist = 0
        for j in day["cal"]:
            if j["UID"] == UID:
                rank = counter
                dist = j["tot_cal"]
                break
            counter = counter + 1

        userRank.append(
            {"rank": rank, "user": temp["name"], "distance": dist})

        return {"rankings": rankings, "userRank": userRank}

    def displayWeeklyCalLeaderboard(UID):
        day = Trip.TripMgr.queryDataWeekly()
        rankings = []
        userRank = []
        counter = 1

        for i in day["cal"]:
            if counter > 20:
                break
            temp = User.UserMgr.getUser(i["UID"])[0]  # fix
            rankings.append(
                {"rank": counter, "user": temp["name"], "distance": i["tot_cal"]})
            counter = counter+1

        temp = User.UserMgr.getUser(UID)[0]  # fix
        rank = -1
        counter = 1
        dist = 0
        for j in day["cal"]:
            if j["UID"] == UID:
                rank = counter
                dist = j["tot_cal"]
                break
            counter = counter + 1

        userRank.append(
            {"rank": rank, "user": temp["name"], "distance": dist})

        return {"rankings": rankings, "userRank": userRank}

    def displayDailyCalLeaderboard(UID):
        day = Trip.TripMgr.queryDataMonthly()
        rankings = []
        userRank = []
        counter = 1

        for i in day["cal"]:
            if counter > 20:
                break
            temp = User.UserMgr.getUser(i["UID"])[0]  # fix
            rankings.append(
                {"rank": counter, "user": temp["name"], "distance": i["tot_cal"]})
            counter = counter+1

        temp = User.UserMgr.getUser(UID)[0]  # fix
        rank = -1
        counter = 1
        dist = 0
        for j in day["cal"]:
            if j["UID"] == UID:
                rank = counter
                dist = j["tot_cal"]
                break
            counter = counter + 1

        userRank.append(
            {"rank": rank, "user": temp["name"], "distance": dist})

        return {"rankings": rankings, "userRank": userRank}


class PostMgr(models.Manager):
    def getLatestPost(self):
        return self.model.objects.order_by("-timestamp").values()


class Post(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    TripID = models.ForeignKey(Trip, on_delete=models.CASCADE)
    # numLikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.UserID)

    objects = models.Manager()
    PostMgr = PostMgr()


class DistAPI(models.Model):
    startLat = models.DecimalField(max_digits=20, decimal_places=15)
    startLng = models.DecimalField(max_digits=20, decimal_places=15)
    endLat = models.DecimalField(max_digits=20, decimal_places=15)
    endLng = models.DecimalField(max_digits=20, decimal_places=15)

    def __str__(self):
        return (self.startLoc, self.endLoc)


class DestAPI(models.Model):
    lat = models.DecimalField(max_digits=20, decimal_places=15)
    lng = models.DecimalField(max_digits=20, decimal_places=15)
    visited = models.PositiveIntegerField(default=0)


class LoopAPI(models.Model):
    lat = models.DecimalField(max_digits=20, decimal_places=15)
    lng = models.DecimalField(max_digits=20, decimal_places=15)
    dist = models.PositiveIntegerField()  # IN METERS


class MapAPIMgr(models.Manager):
    def getWalkingTime(self, org, dest):
        return self.model.gmaps.distance_matrix(mode="walking", origins=org, destinations=dest)["rows"][0]["elements"][0]["duration"]["value"]

    def findLandmark(self, loc, iter, rad=2500):
        o = self.model.gmaps.places_nearby(location={'lat': loc["lat"], 'lng': loc["lng"]}, radius=rad, type=[
            "tourist_attraction", "museum", "park", "stadium"])["results"]
        return {"name": o[iter % (len(o)-1)]["name"], "loc": o[iter % (len(o)-1)]["geometry"]["location"]}

    def findLandmarks(self, loc, rad):
        landmarks = []
        names = []
        g = self.model.gmaps.places_nearby(location={'lat': loc["lat"], 'lng': loc["lng"]}, radius=rad, type=[
            "tourist_attraction", "museum", "park", "stadium"])["results"]
        for i in g:
            landmarks.append(i["geometry"]["location"])
            names.append(i["name"])
        return (names, landmarks)

    def getLegPins(self, startLoc, endLoc, mode):
        polyline = []
        temp = self.model.gmaps.directions(
            origin={'lat': startLoc["lat"], 'lng': startLoc["lng"]}, destination=endLoc, mode=mode)
        direc = object
        for i in temp:
            direc = i["legs"][0]["steps"]
        for i in direc:
            polyline.append(i["polyline"]["points"])
        else:
            pings = i["start_location"]

        return {"polyline": polyline, "pings": pings}

    def getLegPinsAlt(self, startLoc, endLoc, mode):
        polyline = []
        direc = self.model.gmaps.directions(
            origin=startLoc, destination=endLoc, mode=mode, alternatives=True)[-1]["legs"][0]["steps"]
        for i in direc:
            polyline.append(i["polyline"]["points"])
        else:
            pings = i["start_location"]

        return {"polyline": polyline, "pings": pings}

    # def geolocate(self,locName):
    #     temp = self.model.gmaps.geocode(address=locName)
    #     print(temp[0]["geometry"]["location"])
    #     return temp[0]["geometry"]["location"]


class MapAPI(models.Model):
    api = "AIzaSyCiOKHnViKdiOOk3Vv_lQSTRYKJms7OZdY"
    gmaps = googlemaps.Client(key=api)

    objects = models.Manager()
    MapAPIMgr = MapAPIMgr()


class BicycleStandAPIMgr(models.Manager):
    def getBicycleStands(self, location, radius):
        param = {
            "Lat": location["latitude"],
            "Long": location["longitude"],
            "Dist": radius
        }

        response = object
        while(True):
            response = requests.get(
                self.model.url, headers=self.model.head, params=param)
            if(response.json()["value"] != []):
                break
            param["Dist"] = param["Dist"]+0.25

        maxval = 1000
        index = 0
        count = 0

        for i in response.json()["value"]:
            dist = MapAPI.MapAPIMgr.getWalkingTime({"lat": location["latitude"], "lng": location["longitude"]}, {
                "lat": i["Latitude"], "lng": i["Longitude"]})
            if(dist < maxval):
                maxval = dist
                index = count
            count = count + 1

        return response.json()["value"][index]


class BicycleStandAPI(models.Model):
    api = "S8kSh3qPRJWP2m5CvyG/Qw=="
    url = "http://datamall2.mytransport.sg/ltaodataservice/BicycleParkingv2"

    head = {
        "AccountKey": api,
        "accept": "application/json"
    }

    objects = models.Manager()
    BicycleStandAPIMgr = BicycleStandAPIMgr()


class BicycleMgr(models.Model):
    def findNearestStand(self, loc):
        stand_all = BicycleStandAPI.BicycleStandAPIMgr.getBicycleStands(
            loc, 0.20)
        stand = {"latitude": stand_all["Latitude"],
                 "longitude": stand_all["Longitude"]}
        return stand


class BicycleStand(models.Model):
    description = models.TextField()
    location = models.ManyToManyField(Location)
    rackType = models.CharField(max_length=50)
    shelterIndicator = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.rackType

    objects = models.Manager()
    BicycleMgr = BicycleMgr()
