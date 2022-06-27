from collections import defaultdict

data=[
    {
        "nom_troncons":"ierhfgirghih",
        "nom_point_A":"indenie",
        "longitude_point_A":"-4.0224767000",
        "latitude_point_A":"5.3404293000",
        "nom_point_B":"abobo",
        "longitude_point_B":"-4.0290070000",
        "latitude_point_B":"5.4354870000"
    },
    {
        "nom_troncons":"gergerg",
        "nom_point_A":"indenie",
        "longitude_point_A":"-4.0224767000",
        "latitude_point_A":"5.3404293000",
        "nom_point_B":"fraternite matin",
        "longitude_point_B":"-4.0182667000",
        "latitude_point_B":"5.3442390000"
    },

    {
        "nom_troncons":"hrthrthrthththt",
        "nom_point_A":"fraternite matin",
        "longitude_point_A":"-4.0182667000",
        "latitude_point_A":"5.3442390000",
        "nom_point_B":"indenie",
        "longitude_point_B":"-4.0224767000",
        "latitude_point_B":"5.3404293000"
    }
]
thedict = data

d = {}

for item in thedict:
    a = [item["nom_point_A"],item["longitude_point_A"],item["latitude_point_A"]]
    b = [item["nom_point_B"],item["longitude_point_B"],item["latitude_point_B"]]
    d.setdefault(tuple(a), []).append(tuple(b))

list(d.values())
print(d)
visitedList = [[]]
def depthFirst(graph, currentVertex, visited):
    if currentVertex in graph:
        visited.append(currentVertex)
        for vertex in graph[currentVertex]:
            if vertex not in visited:
                depthFirst(graph, vertex, visited.copy())
        visitedList.append(visited)
    else:
        visited.append(currentVertex)
        visitedList.append(visited)

depthFirst(d, ("indenie",'-4.0224767000', '5.3404293000'), [])

l =visitedList
l.pop(0)
del l[-1]
print("les chemins sont",l)