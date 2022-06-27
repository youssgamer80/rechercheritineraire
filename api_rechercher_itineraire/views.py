# Create your views here.
import os

import httpx
from asgiref.sync import sync_to_async
from django.forms import model_to_dict
from rest_framework import status
from decimal import Decimal
import itertools
from trafficduration import trafffic_duration_from_dict
from .class_ors.osr_matrix_duration import osr_matrix_duration_from_dict
from .class_ors.osr_itineraire import osr_itineraire_from_dict
from .serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
import json
import asyncio
from time import sleep
from django.http import HttpResponse
import operator
from django.db.models import Q
from functools import reduce

# visitedList = [[]]
mapBoxApiKey = "sk.eyJ1IjoidmlyZ2lsOTgiLCJhIjoiY2w0aDhvN2ZvMDNqYjNpcGV2amdteXEweCJ9.jxQ0o5aC0tf0S6U8Kze8_Q"
osr_URL_BASE = "http://192.168.252.204:8080/ors/v2"
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
    visitedList = [[]]

    cursor = connection.cursor()
    query = "SELECT t.id AS id_troncons, t.nom AS nom_troncons, a.id AS id_point_A, a.nom AS nom_point_A, a.longitude AS longitude_point_A,a.latitude AS latitude_point_A, b.id AS id_point_B, b.nom AS nom_point_B, b.longitude AS longitude_point_B,b.latitude AS latitude_point_B FROM troncon t LEFT JOIN point_arret a ON t.id_point_arret_A_fk = a.id LEFT JOIN point_arret b ON t.id_point_arret_B_fk = b.id"
    cursor.execute(query)
    res = cursor.fetchall()
    serializer = RawQuerySerializer(res, many=True)
    d = {}
    #print(query)
    itinieraires = []
    #print(json.loads(json.dumps(serializer.data)))
    for item in json.loads(json.dumps(serializer.data)):
        a = [item["nom_point_A"], item["longitude_point_A"], item["latitude_point_A"]]
        b = [item["nom_point_B"], item["longitude_point_B"], item["latitude_point_B"]]
        d.setdefault(tuple(a), []).append(tuple(b))
    list(d.values())
    depthFirst(d, (str(zone), float(lonA), float(latA)), [], visitedList)

    l = visitedList
    print(len(visitedList))
    if len(l) > 0:
        l.pop(0)

    return visitedList


def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


async def write_data(zoneA, lonA, latA):
    fpointArret = []
    fmatrixList = []
    fitineraires = []
    profiles = ['driving-car','cycling-regular','foot-walking']
    for profile in profiles:
        pointArret = []
        matrixList = []
        itineraires = []
        try:
            filePathPointArret = 'point-arret %s %s.json'%(zoneA,profile)
            filePathMatrixDistance= 'matrix-distance %s %s.json' % (zoneA, profile)
            filePathMatrixitineraire = 'itineraire %s %s.json' % (zoneA, profile)

            absolutePathPointArret = '/Users/oda_38/Documents/YooBi/Back-end/rechercherItineraire/api_rechercher_itineraire/itineraires/%s/%s'%(zoneA,filePathPointArret)
            absolutePathMatrixDistance = '/Users/oda_38/Documents/YooBi/Back-end/rechercherItineraire/api_rechercher_itineraire/itineraires/%s/%s' % (zoneA, filePathMatrixDistance)
            absolutePathMatrixItineraire = '/Users/oda_38/Documents/YooBi/Back-end/rechercherItineraire/api_rechercher_itineraire/itineraires/%s/%s' % (zoneA, filePathMatrixitineraire)

            if not os.path.exists('/Users/oda_38/Documents/YooBi/Back-end/rechercherItineraire/api_rechercher_itineraire/itineraires/{}'.format(zoneA)):
                os.makedirs('/Users/oda_38/Documents/YooBi/Back-end/rechercherItineraire/api_rechercher_itineraire/itineraires/{}'.format(zoneA))
            if is_non_zero_file(absolutePathPointArret) == False:

                pa = open(absolutePathPointArret, 'a')
                ma = open(absolutePathMatrixDistance, 'a')
                it = open(absolutePathMatrixItineraire, 'a')
                chemins=  genererChemins(zoneA, lonA, latA)

                pAs = json.loads(json.dumps(chemins))
                for pA in pAs:
                    coords = []
                    for coord in pA:
                        coords.append([coord[1],coord[2]])
                    print(coords)
                    async with httpx.AsyncClient() as client:
                        await asyncio.sleep(1)
                        matrix = osr_URL_BASE + '/matrix/%s'%(profile)
                        r = await client.post(
                            matrix,
                            json={"locations":coords,"metrics":["distance"]}
                        )
                        await asyncio.sleep(1)
                        itineraire = osr_URL_BASE + '/directions/%s/geojson'%(profile)
                        r2 = await client.post(
                            itineraire,
                            json={"coordinates": coords}
                        )
                        if r.status_code == 200:
                            trafficduration = osr_matrix_duration_from_dict(r.json()).distances[0]
                            if(all(x <= y for x,y in zip(trafficduration, trafficduration[1:]))):
                                pointArret.append(pA)
                                matrixList.append(r.json())
                                itineraires.append(r2.json())

                pa.truncate(0)
                pa.write(json.dumps(pointArret))
                pa.close()

                ma.truncate(0)
                ma.write(json.dumps(matrixList))
                ma.close()

                it.truncate(0)
                it.write(json.dumps(itineraires))
                it.close()

        except FileNotFoundError:
            print('File does not exist')

def read_data(zoneA, lonA, latA):

    profiles = ['driving-car','cycling-regular','foot-walking']
    fpointArret = []
    fmatrixList = []
    fitineraires = []
    d = {}
    for profile in profiles:
        pointArret = []
        matrixList = []
        itineraires = []
        try:
            filePathPointArret = 'point-arret %s %s.json'%(zoneA,profile)
            filePathMatrixDistance= 'matrix-distance %s %s.json' % (zoneA, profile)
            filePathMatrixitineraire = 'itineraire %s %s.json' % (zoneA, profile)

            absolutePathPointArret = '/Users/oda_38/Documents/YooBi/Back-end/rechercherItineraire/api_rechercher_itineraire/itineraires/%s/%s'%(zoneA,filePathPointArret)
            absolutePathMatrixDistance = '/Users/oda_38/Documents/YooBi/Back-end/rechercherItineraire/api_rechercher_itineraire/itineraires/%s/%s' % (zoneA, filePathMatrixDistance)
            absolutePathMatrixItineraire = '/Users/oda_38/Documents/YooBi/Back-end/rechercherItineraire/api_rechercher_itineraire/itineraires/%s/%s' % (zoneA, filePathMatrixitineraire)



            pa = open(absolutePathPointArret)
            pointArret = json.load(pa)
            pa.close()

            ma = open(absolutePathMatrixDistance)
            matrixList = json.load(ma)

            ma.close()

            it = open(absolutePathMatrixItineraire)
            itineraires = json.load(it)
            it.close()

            d["%s"%(profile)]={"matrix-distances":matrixList,"points-arrets":pointArret,"itineraires":itineraires}
        except FileNotFoundError:
            print('File does not exist')
    return json.loads(json.dumps(d))

def getInfTroncon(lonA, latA,  lonB, latB):
    cursor =  connection.cursor()
    query = """
    SELECT * FROM

(SELECT t1.type_transport as type_transport, t1.prix_troncon as prix_troncon ,  a.id AS id_point_A, a.nom AS nom_point_A, a.longitude AS longitude_point_A,a.latitude AS latitude_point_A, b.id AS id_point_B, b.nom AS nom_point_B, b.longitude AS longitude_point_B,b.latitude AS latitude_point_B FROM
 
 (SELECT troncon_type_transport.id_troncon_fk as id_troncon_fk,troncon_type_transport.id_type_transport_fk as id_type_transport_fk,troncon.id_point_arret_A_fk,troncon.id_point_arret_B_fk,troncon.id AS id_troncon,type_transport.id as id_type_transport,type_transport.libelle_type_transport AS type_transport,troncon_type_transport.prix AS prix_troncon FROM type_transport,troncon,troncon_type_transport WHERE id_troncon_fk=troncon.id AND id_type_transport_fk=type_transport.id) as t1
 
 LEFT JOIN point_arret a ON t1.id_point_arret_A_fk = a.id
 
 LEFT JOIN point_arret b ON t1.id_point_arret_B_fk = B.id) AS t3 
 
 WHERE
 t3.longitude_point_A=%s AND t3.latitude_point_A=%s  AND t3.longitude_point_B=%s AND t3.latitude_point_B=%s 
    """%(lonA, latA,  lonB, latB)
    #print(query)
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

def check_list(lst):
    ele = lst[0]
    chk = True
    for i in range(len(lst)):
            # Comparing each element with first item
            for k in range(len(lst)):
                if k!=i:
                    if lst[i] != lst[k] :
                        chk = False
                        print(lst[i] != lst[k])
                        break

            if not chk:
                print("Not equal",i)
            else:
                print("Equal")



async def genItineraire( zoneA, lonA, latA, zoneB, lonB, latB,profile):
    pointarretsR = []
    pointarret = []
    infosToncon =[]
    combinaisonInfos =[]
    combinaisonPoints = []
    combinaisonMatrix = []
    combinaisonItineraire = []
    resp = []
    index = []
    matrixR = []
    matrix =[]
    itinerairesR = []
    itineraires = []
    if (lonA, latA) == (lonB, latB):
        return Response({"data": []}, status=status.HTTP_200_OK)
    else:

        if not os.path.exists(
                '/Users/oda_38/Documents/YooBi/Back-end/rechercherItineraire/api_rechercher_itineraire/itineraires/{}'.format(
                        zoneA)):
            await write_data(zoneA, lonA, latA)

        else:
            response = read_data(zoneA, lonA, latA)
            #print(response)
            pointarret = response[profile]["points-arrets"]
            itineraires = response[profile]["itineraires"]
            matrix = response[profile]["matrix-distances"]




        pointarretsR = [t for t in pointarret if [t[-1][1],t[-1][2] ] == [float(lonB), float(latB)] ]



        for resultat in pointarretsR:
            matrixR.append(matrix[pointarret.index(resultat)])
            itinerairesR.append(itineraires[pointarret.index(resultat)])



        infos =[]
        isLast = False
        for resultat in pointarretsR:
            infos = []
            for i in range(len(resultat)):
                if i==len(resultat)-1:
                    break
                else:
                    #print(resultats[0])
                    #print((resultat[i][0],resultat[i+1][0]))

                    infos.append((getInfTroncon(resultat[i][1],resultat[i][2],resultat[i+1][1],resultat[i+1][2])))
            infosToncon.append(infos)
            #casser les itineraires avec un troncons comportant plusieurs type de transport
            for infos in infosToncon:
                combinaisonInfos.append(list(itertools.product(*infos)))
                combinaisonPoints.append(pointarretsR[infosToncon.index(infos)])
                combinaisonMatrix.append(matrixR[infosToncon.index(infos)])
                combinaisonItineraire.append(itinerairesR[infosToncon.index(infos)])
        #print(infosToncon)


        #print(check_list(infosToncon))
        pointarretsR = combinaisonPoints
        infosToncon = combinaisonInfos
        itinerairesR = combinaisonItineraire
        matrixR = combinaisonMatrix

    return list(reversed(pointarretsR)),list(reversed(infosToncon)),list(reversed(itinerairesR)),list(reversed(matrixR))

async def getCheminasync( zoneA, lonA, latA, zoneB, lonB, latB,profile):
        resultats = []
        infosToncon = []
        itinerairesR = []
        matrixR = []
        resp = []
        durationsMatrix = []
        resultats,infosToncon,itinerairesR,matrixR =await genItineraire(zoneA, lonA, latA, zoneB, lonB, latB,profile)
        r = {}

        """for resultat in resultats:
            coord =""
            curbs=""
            for re in resultat:
                if(resultat.index(re)!=len(resultat)-1):
                    coord += str(re[1])+","+str(re[2])+";"
                    curbs += "curb;"
                else:
                    coord += str(re[1])+","+ str(re[2])
                    curbs += "curb"

            async with httpx.AsyncClient() as client:
                await asyncio.sleep(1)
                q = "https://api.mapbox.com/directions-matrix/v1/mapbox/driving-traffic/%s?approaches=%s&access_token=%s"%(coord,curbs,mapBoxApiKey)
                r = await client.get(q)
                if r.status_code == 200:
                   trafficduration=    trafffic_duration_from_dict(r.json()).durations
                   durationsMatrix.append(trafficduration)
        print (durationsMatrix)"""
        print(len(resultats))
        print(len(infosToncon))
        print(len(itinerairesR))
        print(len(matrixR))
        resp.append({"points-arrets":resultats,"details-itineraires":infosToncon,"itineraires":itinerairesR,"matrix-durees":matrixR})

        return resp

async def getChemin(request, zoneA, lonA, latA, zoneB, lonB, latB,profile):
    tasks =  await getCheminasync(zoneA, lonA, latA, zoneB, lonB, latB,profile)
    response = {"data":tasks}
    #return HttpResponse(tasks)
    return HttpResponse(json.dumps(response), content_type="application/json")


def sort_key(item):
    return item[0].features[0].properties.summary.distance
async def filtre(request,index,type,filtre, zoneA, lonA, latA, zoneB, lonB, latB,profile):
    pointsfiltre = []
    points = []
    infosToncon = []
    trouve = True
    resutats = []
    itinerairesR = []
    matrixR = []
    indexofitineraire = []
    points = []

    beforeFilterPoints = []
    afterFilterPoints = []

    beforeFilterItineraires = []
    afterFilterItineraires= []

    beforeFilterMatrix = []
    afterFilterMatrix = []

    beforeFilterDetailsItineraire= []
    afterFilterDetailsItineraire = []

    points, infosToncon,itinerairesR,matrixR = await genItineraire(zoneA, lonA, latA, zoneB, lonB, latB,profile)
    print(type)
    # Here you list all your filter names
    #filter_names = ["distance-temps","distance-prix","prix-temps","temps-distance","prix-distance","temps-prix","vide-vide"]
    #filter_priority = filter_names[0].split('-')[0]
    filter_priority = filtre.split('-')[0]
    print('--------------',filter_priority)
    if index !="0":
        for itineraire in infosToncon:
            trouve = True
            for troncons in itineraire:
                if trouve:
                    if type.lower() == "gbaka".lower() or type.lower() == "warren".lower():
                        if type.lower() in [x["type_transport"].lower() for x in troncons]:
                            trouve = True
                        else:
                            trouve = False
                    else:
                        if not [x for x in troncons]:
                            trouve = True
                        else:
                            trouve = False
                else:
                    break
            if trouve:
                resutats.append(itineraire)
                indexofitineraire.append(infosToncon.index(itineraire))

        for itineraire in resutats:
            for troncons in itineraire:
                resutats[resutats.index(itineraire)][resutats[resutats.index(itineraire)].index(troncons)] = [t for t in troncons if t["type_transport"].lower() == type.lower()]
        m =[]
        i = []
        print(resutats)
        for index in indexofitineraire:
            pointsfiltre.append(points[index])
            m.append(matrixR[index])
            i.append(itinerairesR[index])

        points = pointsfiltre
        infosToncon = resutats
        itinerairesR = i
        matrixR = m

    if filter_priority !="vide":

        match filter_priority:
            case "Moinslong":

                for itineraire in itinerairesR:
                    beforeFilterItineraires.append(osr_itineraire_from_dict(itineraire))

                filter_list = sorted(beforeFilterItineraires,key=lambda x: x.features[0].properties.summary.distance, reverse=True)
                for after in filter_list:
                    afterFilterMatrix.append(matrixR[beforeFilterItineraires.index(after)])
                    afterFilterPoints.append(points[beforeFilterItineraires.index(after)])
                    afterFilterDetailsItineraire.append(infosToncon[beforeFilterItineraires.index(after)])
                    afterFilterItineraires.append(itinerairesR[beforeFilterItineraires.index(after)])



            case "Moinscoûteux":
                print("")
            case "temps":

                for itineraire in itinerairesR:
                    beforeFilterItineraires.append(osr_itineraire_from_dict(itineraire))

                filter_list = sorted(beforeFilterItineraires,key=lambda x: x.features[0].properties.summary.duration, reverse=True)
                for after in filter_list:
                    afterFilterMatrix.append(matrixR[beforeFilterItineraires.index(after)])
                    afterFilterPoints.append(points[beforeFilterItineraires.index(after)])
                    afterFilterDetailsItineraire.append(infosToncon[beforeFilterItineraires.index(after)])
                    afterFilterItineraires.append(itinerairesR[beforeFilterItineraires.index(after)])
    else:
        afterFilterMatrix = matrixR
        afterFilterPoints = points
        afterFilterDetailsItineraire = infosToncon
        afterFilterItineraires = itinerairesR

    to_return = {"points-arrets":list(reversed(afterFilterPoints)),"details-itineraires":list(reversed(afterFilterDetailsItineraire)),"itineraires":list(reversed(afterFilterItineraires)),"matrix-durees":list(reversed(afterFilterMatrix))}
    return HttpResponse(json.dumps({"data":[to_return]}), content_type="application/json")