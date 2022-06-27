# Create your views here.
import os
from collections import defaultdict
from itertools import groupby

from rest_framework import status
from decimal import Decimal

from .serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
import asyncio
import json

dbdata=             [
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "etrgrg",
                    "prix_troncon": 100.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "etrgrg",
                    "prix_troncon": 200.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "etrgrg",
                    "prix_troncon": 400.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "etrgrg",
                    "prix_troncon": 150.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "thgthte",
                    "prix_troncon": 100.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "thgthte",
                    "prix_troncon": 200.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "thgthte",
                    "prix_troncon": 400.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "thgthte",
                    "prix_troncon": 150.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Train",
                    "prix_troncon": 100.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Train",
                    "prix_troncon": 200.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Train",
                    "prix_troncon": 400.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Train",
                    "prix_troncon": 150.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "camion1",
                    "prix_troncon": 100.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "camion1",
                    "prix_troncon": 200.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "camion1",
                    "prix_troncon": 400.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "camion1",
                    "prix_troncon": 150.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "test",
                    "prix_troncon": 100.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "test",
                    "prix_troncon": 200.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "test",
                    "prix_troncon": 400.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "test",
                    "prix_troncon": 150.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "test",
                    "prix_troncon": 100.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "test",
                    "prix_troncon": 200.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "test",
                    "prix_troncon": 400.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "test",
                    "prix_troncon": 150.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Warren1",
                    "prix_troncon": 100.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Warren1",
                    "prix_troncon": 200.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Warren1",
                    "prix_troncon": 400.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Warren1",
                    "prix_troncon": 150.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Warren5",
                    "prix_troncon": 100.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Warren5",
                    "prix_troncon": 200.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Warren5",
                    "prix_troncon": 400.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Warren5",
                    "prix_troncon": 150.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Gbaka",
                    "prix_troncon": 100.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Gbaka",
                    "prix_troncon": 200.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Gbaka",
                    "prix_troncon": 400.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Gbaka",
                    "prix_troncon": 150.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Gajgjdj",
                    "prix_troncon": 100.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Gajgjdj",
                    "prix_troncon": 200.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Gajgjdj",
                    "prix_troncon": 400.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                },
                {
                    "id_point_A": 2,
                    "longitude_point_A": -4.0182667,
                    "latitude_point_A": 5.344239,
                    "nom_point_A": "fraternite",
                    "type_transport": "Gajgjdj",
                    "prix_troncon": 150.0,
                    "id_point_B": 3,
                    "longitude_point_B": -4.029007,
                    "latitude_point_B": 5.435487,
                    "nom_point_B": "abobo"
                }
            ]
# visitedList = [[]]
def depthFirst(graph, currentVertex, visited, visitedList):

    if currentVertex in graph:
        visited.append(currentVertex)
        for vertex in graph[currentVertex]:
            if vertex not in visited:
                depthFirst(graph, vertex, visited.copy(), visitedList)
        visitedList.append(visited)
        return visitedList
    else:
        visited.append(currentVertex)
        visitedList.append(visited)
        return visitedList



def genererChemins(zone, lonA, latA):
    finish = True
    print(type(lonA))
    visitedList = [[]]

    cursor = connection.cursor()
    query = "SELECT t.id AS id_troncons, t.nom AS nom_troncons, a.id AS id_point_A, a.nom AS nom_point_A, a.longitude AS longitude_point_A,a.latitude AS latitude_point_A, b.id AS id_point_B, b.nom AS nom_point_B, b.longitude AS longitude_point_B,b.latitude AS latitude_point_B FROM troncon t LEFT JOIN point_arret a ON t.id_point_arret_A_fk = a.id LEFT JOIN point_arret b ON t.id_point_arret_B_fk = b.id"
    cursor.execute(query)
    res = cursor.fetchall()
    serializer = RawQuerySerializer(res, many=True)
    d = {}
    for item in json.loads(json.dumps(serializer.data)):
        a = [item["nom_point_A"], item["longitude_point_A"], item["latitude_point_A"]]
        b = [item["nom_point_B"], item["longitude_point_B"], item["latitude_point_B"]]
        d.setdefault(tuple(a), []).append(tuple(b))
    list(d.values())
    depthFirst(d, (str(zone), float(lonA), float(latA)), [], visitedList)
    print("last item", visitedList.pop())

    print(d)
    l = visitedList
    if len(l) > 0:
        l.pop(0)
    print("les chemins sont", visitedList)
    return visitedList


def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


def write_read_data(zoneA, lonA, latA):
    data =[]
    try:
        filePath = '{}.json'.format(zoneA)
        absolutePath = '/Users/oda_38/Documents/YooBi/Back-end/rechercherItineraire/api_rechercher_itineraire/{}'.format(
            filePath)
        if is_non_zero_file(absolutePath) == False:
            f = open(absolutePath, 'a')
            chemins= genererChemins(zoneA, lonA, latA)
            data = chemins
            d = json.dumps(chemins)
            f.truncate(0)
            # write to json file
            f.write(d)
            f.close()
        else:
            f = open(absolutePath)
            data = json.load(f)
        f.close()
    except FileNotFoundError:
        print('File does not exist')
    return data


def getInfTroncon(lonA, latA,  lonB, latB):
    cursor = connection.cursor()
    query = """
    SELECT*FROM(SELECT t1.type_transport as type_transport, t1.prix_troncon as prix_troncon , a.id AS id_point_A, a.nom AS nom_point_A, a.longitude AS longitude_point_A,a.latitude AS latitude_point_A, b.id AS id_point_B, b.nom AS nom_point_B, b.longitude AS longitude_point_B,b.latitude AS latitude_point_B FROM(SELECT troncon.id_point_arret_A_fk,troncon.id_point_arret_B_fk,troncon.id AS id_troncon,type_transport.libelle_type_transport AS type_transport,troncon_type_transport.prix AS prix_troncon FROM type_transport,troncon,troncon_type_transport) as t1 LEFT JOIN point_arret a ON t1.id_point_arret_A_fk = a.id LEFT JOIN point_arret b ON t1.id_point_arret_B_fk = B.id) AS t3 WHERE t3.longitude_point_A=%s AND t3.latitude_point_A=%s  AND t3.longitude_point_B=%s  AND t3.latitude_point_B=%s
    """%(lonA, latA,  lonB, latB)
    print(query)
    cursor.execute(query)
    res = cursor.fetchall()
    serializer = TronconInfoSerializer(res, many=True)
    data = json.loads(json.dumps(serializer.data, cls=JSONEncoder))
    return data


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def key_func(k):
    return k['type_transport']


# sort INFO data by 'company' key.


@api_view(["GET"])
def getChemin(self, zoneA, lonA, latA, zoneB, lonB, latB):
    data = []
    infosToncon =[]
    resp = []
    if (lonA, latA) == (lonB, latB):
        return Response({"data": []}, status=status.HTTP_200_OK)
    else:

        data = write_read_data(zoneA, lonA, latA)

        resultat = [t for t in data if [t[-1][1],t[-1][2] ] == [float(lonB), float(latB)] ]
        for r in resultat:
            latA=0,
            lonA=0,
            latB=0,
            lonB=0,
            isLast =False
            t = []
            for i in range(len(r)):

                if i==len(r)-1:
                    isLast=True

                else:

                    lonA = r[i][1]
                    latA = r[i][2]
                    lonB = r[i+1][1]
                    latB = r[i+1][2]
                    t.append(getInfTroncon(lonA, latA,  lonB, latB))
            infosToncon.append(t)

            if isLast:
                break

        resp.append(resultat)
        resp.append(infosToncon)
        d = {}
        INFO = sorted(dbdata, key=key_func)
        resd = defaultdict(list)

        for key, value in groupby(INFO, key_func):
            d.setdefault(key, []).append(list(value))
            print(key)
            print(list(d.values()))
        return Response({"data": d}, status=status.HTTP_200_OK)
