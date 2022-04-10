"""GoBikes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# url was removed in Django 4.0, hencewe use path/re_path (RegEx)
from django.urls import path, include, re_path
from . import views
from rest_framework import routers
# For JWT Authentication
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

router = routers.DefaultRouter()
router.register("User", views.UserView)
router.register("Target", views.TargetView)
# router.register("Location", views.LocationView)
router.register("Trip", views.TripView)
#router.register("Statistics", views.StatisticsView)
router.register("Post", views.PostView)
# router.register("BicycleStand", views.BicycleStandView)
router.register("DistAPI", views.DistAPIView)
router.register("DestAPI", views.DestAPIView)
router.register("LoopAPI", views.LoopAPIView)
router.register("Pings", views.GPSPingsView)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # re_path(r'^auth/users/activation/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$',
    #         views.UserActivationView.as_view()),
    # # Handles User Activation
    # path('auth/', include('djoser.urls.authtoken')),
    # For Django AuthToken Authentication
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # # For JWT Authentication
]
