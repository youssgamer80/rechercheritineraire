from .views import *
from django.urls import path, include

urlpatterns = [
    path('troncon/<str:zone>/<str:zoneA>/<str:lonA>/<str:latA>/<str:zoneB>/<str:lonB>/<str:latB>/<str:profile>',getChemin, name="troncon-list"),
    path('troncon/filtre/<str:index>/<str:type>/<str:filtre>/<str:zone>/<str:zoneA>/<str:lonA>/<str:latA>/<str:zoneB>/<str:lonB>/<str:latB>/<str:profile>',filtre, name="filtre"),
    path('generate',generateAllPointIntineraire, name="generation"),

]