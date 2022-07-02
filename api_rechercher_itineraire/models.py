# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Appartenir(models.Model):
    id_ligne_fk = models.ForeignKey('Ligne', models.DO_NOTHING, db_column='id_ligne_fk')
    id_troncon_fk = models.ForeignKey('Troncon', models.DO_NOTHING, db_column='id_troncon_fk')
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'appartenir'


class Avoir(models.Model):
    id_itineraire_fk = models.ForeignKey('Itineraire', models.DO_NOTHING, db_column='id_itineraire_fk', blank=True, null=True)
    id_mode_deplacement_fk = models.ForeignKey('ModeDeplacement', models.DO_NOTHING, db_column='id_mode_deplacement_fk', blank=True, null=True)
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'avoir'


class Borne(models.Model):
    libelle = models.CharField(max_length=255)
    id_point_arret_fk = models.ForeignKey('PointArret', models.DO_NOTHING, db_column='id_point_arret_fk')
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'borne'


class Chauffeur(models.Model):
    nom = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    cni = models.CharField(max_length=255, blank=True, null=True)
    permis = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=10, blank=True, null=True)
    statut = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chauffeur'


class Conduire(models.Model):
    id_vehicule = models.ForeignKey('Vehicule', models.DO_NOTHING, db_column='id_vehicule', blank=True, null=True)
    id_chauffeur = models.ForeignKey(Chauffeur, models.DO_NOTHING, db_column='id_chauffeur', blank=True, null=True)
    date = models.DateField()
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'conduire'


class Constituer(models.Model):
    id_itineraire_fk = models.ForeignKey('Itineraire', models.DO_NOTHING, db_column='id_itineraire_fk')
    id_troncon_fk = models.ForeignKey('Troncon', models.DO_NOTHING, db_column='id_troncon_fk')
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'constituer'


class Demande(models.Model):
    code_demande = models.CharField(unique=True, max_length=255, blank=True, null=True)
    etat = models.IntegerField(blank=True, null=True)
    id_proprietaire_fk = models.ForeignKey('Proprietaire', models.DO_NOTHING, db_column='id_proprietaire_fk')
    date = models.DateTimeField()
    statut = models.IntegerField()
    id_zone_fk = models.ForeignKey('Zone', models.DO_NOTHING, db_column='id_zone_fk')
    id_type_transport_fk = models.ForeignKey('TypeTransport', models.DO_NOTHING, db_column='id_type_transport_fk')
    immatriculation = models.CharField(max_length=255)
    marque = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    nb_place = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'demande'


class DemanderItineraire(models.Model):
    id_itineraire_fk = models.ForeignKey('Itineraire', models.DO_NOTHING, db_column='id_itineraire_fk')
    id_client_fk = models.ForeignKey('Usager', models.DO_NOTHING, db_column='id_client_fk')
    date = models.DateTimeField()
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'demander_itineraire'


class Emprunter(models.Model):
    id_troncon_fk = models.ForeignKey('Troncon', models.DO_NOTHING, db_column='id_troncon_fk')
    id_vehicule_fk = models.ForeignKey('Vehicule', models.DO_NOTHING, db_column='id_vehicule_fk')
    date_arrivee = models.DateTimeField()
    date_depart = models.DateTimeField()
    id_client_fk = models.ForeignKey('Usager', models.DO_NOTHING, db_column='id_client_fk')
    date = models.DateTimeField()
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'emprunter'


class Itineraire(models.Model):
    temps = models.DateTimeField()
    tarif = models.FloatField(blank=True, null=True)
    distance = models.IntegerField(blank=True, null=True)
    id_trajet_fk = models.ForeignKey('Trajet', models.DO_NOTHING, db_column='id_trajet_fk', blank=True, null=True)
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'itineraire'


class Ligne(models.Model):
    nom = models.CharField(max_length=255)
    depart = models.CharField(max_length=255)
    arrivee = models.CharField(max_length=255)
    id_type_transport_fk = models.ForeignKey('TypeTransport', models.DO_NOTHING, db_column='id_type_transport_fk')
    id_zone_fk = models.ForeignKey('Zone', models.DO_NOTHING, db_column='id_zone_fk')
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ligne'


class ModeDeplacement(models.Model):
    mode_deplacement = models.CharField(max_length=255, blank=True, null=True)
    statut = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mode_deplacement'


class Permission(models.Model):
    permission = models.CharField(max_length=255)
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'permission'


class PointArret(models.Model):
    nom = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    statut = models.IntegerField(blank=True, null=True)
    id_zone_fk = models.ForeignKey('zone', models.DO_NOTHING, db_column='id_zone_fk')

    class Meta:
        managed = False
        db_table = 'point_arret'
        unique_together = (('longitude', 'latitude'),)


class Posseder(models.Model):
    periode = models.DateTimeField()
    statut = models.IntegerField()
    id_vehicule_fk = models.ForeignKey('Vehicule', models.DO_NOTHING, db_column='id_vehicule_fk')
    id_trackergps_fk = models.ForeignKey('Trackergps', models.DO_NOTHING, db_column='id_trackergps_fk')

    class Meta:
        managed = False
        db_table = 'posseder'


class PossederTrackergps(models.Model):
    periode = models.DateTimeField()
    statut = models.IntegerField()
    id_vehicule_fk = models.PositiveIntegerField()
    id_trackergps_fk = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'posseder-trackergps'


class PossederVehicule(models.Model):
    id_proprietaire_fk = models.ForeignKey('Proprietaire', models.DO_NOTHING, db_column='id_proprietaire_fk')
    id_vehicule_fk = models.ForeignKey('Vehicule', models.DO_NOTHING, db_column='id_vehicule_fk')
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'posseder-vehicule'


class Proprietaire(models.Model):
    nom = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    statut = models.IntegerField(blank=True, null=True)
    permis = models.CharField(max_length=255, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    genre = models.CharField(max_length=1)
    lieu_naissance = models.CharField(max_length=255, blank=True, null=True)
    lieu_residence = models.CharField(max_length=255)
    piece_identite = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'proprietaire'


class Role(models.Model):
    role = models.CharField(max_length=255)
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'role'


class RolePermission(models.Model):
    id_role_fk = models.ForeignKey(Role, models.DO_NOTHING, db_column='id_role_fk')
    id_permission_fk = models.ForeignKey(Permission, models.DO_NOTHING, db_column='id_permission_fk')
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'role-permission'


class Stationner(models.Model):
    id_vehicule_fk = models.ForeignKey('Vehicule', models.DO_NOTHING, db_column='id_vehicule_fk', blank=True, null=True)
    id_point_arret_fk = models.ForeignKey(PointArret, models.DO_NOTHING, db_column='id_point_arret_fk', blank=True, null=True)
    date = models.DateTimeField()
    id_client_fk = models.ForeignKey('Usager', models.DO_NOTHING, db_column='id_client_fk')
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stationner'


class Token(models.Model):
    token = models.CharField(max_length=255)
    id_proprietaire_fk = models.ForeignKey(Proprietaire, models.DO_NOTHING, db_column='id_proprietaire_fk')
    id_vehicule_fk = models.ForeignKey('Vehicule', models.DO_NOTHING, db_column='id_vehicule_fk')
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'token'


class Trackergps(models.Model):
    libelle = models.CharField(max_length=255)
    id_vehicule_fk = models.ForeignKey('Vehicule', models.DO_NOTHING, db_column='id_vehicule_fk')
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'trackergps'


class Trajet(models.Model):
    depart = models.CharField(max_length=255, blank=True, null=True)
    destination = models.CharField(max_length=255, blank=True, null=True)
    statut = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trajet'


class Troncon(models.Model):
    nom = models.CharField(max_length=255)
    id_point_arret_a_fk = models.ForeignKey(PointArret, models.DO_NOTHING, db_column='id_point_arret_A_fk', related_name="idPointArretA")  # Field name made lowercase.
    id_point_arret_b_fk = models.ForeignKey(PointArret, models.DO_NOTHING, db_column='id_point_arret_B_fk', related_name="idPointArretB")  # Field name made lowercase.
    distance = models.FloatField()
    duree = models.IntegerField()
    tarif = models.DecimalField(max_digits=10, decimal_places=2)
    statut = models.IntegerField()
    id_ligne_fk = models.ForeignKey(Ligne, models.DO_NOTHING, db_column='id_ligne_fk', blank=True, null=True)
    rang = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'troncon'
        unique_together = (('id_point_arret_a_fk', 'id_point_arret_b_fk', 'id_ligne_fk'),)


class TypeTransport(models.Model):
    libelle_type_transport = models.CharField(max_length=255, blank=True, null=True)
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'type_transport'


class TypeZone(models.Model):
    libelle = models.CharField(max_length=255)
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'type_zone'


class Usager(models.Model):
    nom = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    statut = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usager'


class Utilisateur(models.Model):
    nom_utilisateur = models.CharField(max_length=255)
    mot_de_passe = models.CharField(max_length=255)
    id_role_fk = models.ForeignKey(Role, models.DO_NOTHING, db_column='id_role_fk')
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'utilisateur'


class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=255, blank=True, null=True)
    marque = models.CharField(max_length=255, blank=True, null=True)
    modele = models.CharField(max_length=255, blank=True, null=True)
    id_proprietaire_fk = models.ForeignKey(Proprietaire, models.DO_NOTHING, db_column='id_proprietaire_fk', blank=True, null=True)
    statut = models.IntegerField(blank=True, null=True)
    id_type_transport_fk = models.ForeignKey(TypeTransport, models.DO_NOTHING, db_column='id_type_transport_fk', blank=True, null=True)
    nb_place = models.IntegerField(blank=True, null=True)
    id_zone_fk = models.ForeignKey('Zone', models.DO_NOTHING, db_column='id_zone_fk')
    carte_grise = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'vehicule'


class Zone(models.Model):
    id = models.IntegerField(primary_key=True,db_column='id')
    libelle = models.CharField(max_length=255)
    id_type_zone_fk = models.ForeignKey(TypeZone, models.DO_NOTHING, db_column='id_type_zone_fk')
    id_zoneparent_fk = models.ForeignKey('Zoneparent', models.DO_NOTHING, db_column='id_zoneparent_fk')
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zone'


class Zoneparent(models.Model):
    zoneparent = models.CharField(max_length=255)
    statut = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'zoneparent'

class PointZone(models.Model):
    id = models.IntegerField(primary_key=True,db_column='id')
    libelle = models.CharField(max_length=255)
    id_type_zone_fk = models.ForeignKey(TypeZone, models.DO_NOTHING, db_column='id_type_zone_fk')
    id_zoneparent_fk = models.ForeignKey('Zoneparent', models.DO_NOTHING, db_column='id_zoneparent_fk')
    nom = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    id_zone_fk = models.ForeignKey('zone', models.DO_NOTHING, db_column='id_zone_fk')

