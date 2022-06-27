import itertools

data =     [
                    [
                        {
                            "id_point_A": 13,
                            "longitude_point_A": -4.0745688,
                            "latitude_point_A": 5.3541741,
                            "nom_point_A": "Siporex",
                            "type_transport": "Gbaka",
                            "prix_troncon": 100.0,
                            "id_point_B": 14,
                            "longitude_point_B": -4.0719546,
                            "latitude_point_B": 5.3485916,
                            "nom_point_B": "Figayo"
                        }
                    ],
                    [

                        {
                            "id_point_A": 14,
                            "longitude_point_A": -4.0719546,
                            "latitude_point_A": 5.3485916,
                            "nom_point_A": "Figayo",
                            "type_transport": "Gbaka",
                            "prix_troncon": 100.0,
                            "id_point_B": 16,
                            "longitude_point_B": -4.072925,
                            "latitude_point_B": 5.3467062,
                            "nom_point_B": "Pharmacie Keneya"
                        }
                    ],
                    [
                        {
                            "id_point_A": 16,
                            "longitude_point_A": -4.072925,
                            "latitude_point_A": 5.3467062,
                            "nom_point_A": "Pharmacie Keneya",
                            "type_transport": "Warren",
                            "prix_troncon": 200.0,
                            "id_point_B": 20,
                            "longitude_point_B": -4.0587784,
                            "latitude_point_B": 5.3405566,
                            "nom_point_B": "Pharmacie Les Beatitudes"
                        }
                    ]
                ]
combinaison = list(itertools.product(*data))
print(combinaison)
print(len(combinaison))
a = [1,2,3]
num_repeats = 3

a_expanded = a * num_repeats
a_expanded.sort()
print(a_expanded)