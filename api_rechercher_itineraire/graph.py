from collections import defaultdict

"""data=[
  {
    "id_troncon": 2,
    "nom_troncon": "troncon-indenie-fratmat",
    "id_point_A": 1,
    "nom_point_A": "indenie",
    "longitude_point_A": -4.0224767,
    "latitude_point_A": 5.3404293,
    "id_point_B": 2,
    "nom_point_B": "fraternite matin",
    "longitude_point_B": -4.0182667,
    "latitude_point_B": 5.344239
  },
  {
    "id_troncon": 7,
    "nom_troncon": "troncon-fratmat-abobo",
    "id_point_A": 2,
    "nom_point_A": "fraternite matin",
    "longitude_point_A": -4.0182667,
    "latitude_point_A": 5.344239,
    "id_point_B": 3,
    "nom_point_B": "abobo",
    "longitude_point_B": -4.029007,
    "latitude_point_B": 5.435487
  },
  {
    "id_troncon": 8,
    "nom_troncon": "troncon-abobo-indenie",
    "id_point_A": 2,
    "nom_point_A": "fraternite matin",
    "longitude_point_A": -4.0182667,
    "latitude_point_A": 5.344239,
    "id_point_B": 1,
    "nom_point_B": "indenie",
    "longitude_point_B": -4.0224767,
    "latitude_point_B": 5.3404293
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

depthFirst(d, ("fraternite matin",-4.0182667, 5.344239), [])

l =visitedList
l.pop(0)
del l[-1]
print("les chemins sont",l)
"""

graph = { 0 : [1, 2],
          1 : [3, 6, 0],
          2 : [4, 5, 0],
          3 : [1],
          4 : [6, 2],
          5 : [6, 2],
          6 : [1, 4, 5]}
visitedList = [[]]

def depthFirst(graph, currentVertex, visited):
    visited.append(currentVertex)
    for vertex in graph[currentVertex]:
        if vertex not in visited:
            depthFirst(graph, vertex, visited.copy())
    visitedList.append(visited)

depthFirst(graph, 0, [])

print(visitedList)
