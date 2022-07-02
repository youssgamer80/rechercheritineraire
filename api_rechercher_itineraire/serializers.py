from rest_framework import serializers
from api_rechercher_itineraire.models import *
from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField

class TronconSerializer(serializers.ModelSerializer):
    class Meta:
        model = Troncon
        fields = ['nom', 'id_point_arret_a_fk', 'id_point_arret_b_fk']


class PointArretSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointArret
        fields = '__all__'

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'



class PointZoneSerialzer(Serializer):
    zone =SerializerMethodField()
    nom = SerializerMethodField()
    longitude = SerializerMethodField()
    latitude= SerializerMethodField()
    """PointArret"""
    def get_nom(self, instance):
        return instance[1]
    def get_longitude(self, instance):
        return instance[2]
    def get_latitude(self, instance):
        return instance[3]

    """Zone"""
    def get_zone(self,instance):
        return instance[7]



class RawQuerySerializer(Serializer):
    id_troncon = SerializerMethodField()
    nom_troncon = SerializerMethodField()
    id_point_A = SerializerMethodField()
    nom_point_A = SerializerMethodField()
    longitude_point_A = SerializerMethodField()
    latitude_point_A = SerializerMethodField()

    id_point_B = SerializerMethodField()
    nom_point_B = SerializerMethodField()
    longitude_point_B = SerializerMethodField()
    latitude_point_B = SerializerMethodField()

    def get_id_troncon(self, obj):
        return obj[0]

    def get_nom_troncon(self, obj):
        return obj[1]

    def get_id_point_A(self, obj):
        return obj[2]

    def get_nom_point_A(self, obj):
        return obj[3]

    def get_longitude_point_A(self, obj):
        return obj[4]

    def get_latitude_point_A(self, obj):
        return obj[5]

    def get_id_point_B(self, obj):
        return obj[6]

    def get_nom_point_B(self, obj):
        return obj[7]

    def get_longitude_point_B(self, obj):
        return obj[8]

    def get_latitude_point_B(self, obj):
        return obj[9]


class TronconInfoSerializer(Serializer):
    id_point_A = SerializerMethodField()
    longitude_point_A = SerializerMethodField()
    latitude_point_A = SerializerMethodField()
    nom_point_A = SerializerMethodField()

    type_transport = SerializerMethodField()
    prix_troncon = SerializerMethodField()

    id_point_B = SerializerMethodField()
    longitude_point_B = SerializerMethodField()
    latitude_point_B = SerializerMethodField()
    nom_point_B = SerializerMethodField()

    def get_id_point_A(self, obj):
        return obj[2]

    def get_nom_point_A(self, obj):
        return obj[3]

    def get_longitude_point_A(self, obj):
        return obj[4]

    def get_latitude_point_A(self, obj):
        return obj[5]

    def get_type_transport(self, obj):
        return obj[0]

    def get_prix_troncon(self, obj):
        return obj[1]

    def get_id_point_B(self, obj):
        return obj[6]

    def get_longitude_point_B(self, obj):
        return obj[8]

    def get_latitude_point_B(self, obj):
        return obj[9]

    def get_nom_point_B(self, obj):
        return obj[7]
