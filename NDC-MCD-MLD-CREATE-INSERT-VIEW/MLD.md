# Description
Le Modèle Logique des Données(MLD) est simplement la représentation textuelle du MCD. Il s’agit juste de la représentation en ligne du schéma représentant la structure de la base de données.

# Schéma relationnel

+ Musée_Extérieur(#nom: String, adresse:JSON) avec adresse NOT NULL

+ Auteur(#nom: String, #prénom: String, #naissance: Date, mort: Date)
 
+ Exposition_Permanante(#nom: String)

+ Exposition_Temporaire(#nom: String, début: Date, fin: Date) avec début NOT NULL, fin NOT NULL

+ Oeuvre_Louvre(#titre: String, #date: Date, dimension: JSON, deja_empruntée: Boolean, type_oeuvre: String, nom_auteur=>Auteur.nom, prénom_auteur=>Auteur.prénom, naissance_auteur=>Auteur.naissance, exposition=>Exposition_Permanante.nom, prix: Decimal) avec type_oeuvre NOT NULL, deja_empruntée NOT NULL, prix NOT NULL, CHECK type_oeuvre IN ('Peinture','Sculpture', 'photographies')

+ Oeuvre_Ext(#titre: String, #date: Date, dimension: JSON, déja_empruntée: Boolean, type_oeuvre: String, nom_auteur=>Auteur.nom, prénom_auteur=>Auteur.prénom, naissance_auteur=>Auteur.naissance, exposition=>Exposition_Temporaire.nom) avec type_oeuvre NOT NULL, deja_empruntée NOT NULL, exposition NOT NULL, CHECK type_oeuvre IN ('Peinture','Sculpture', 'photographies')

+ Emprunt(début: Date, fin: Date, #musée=>Musée_Extérieur.nom, #titre_oeuvre=>Oeuvre_Ext.titre, #date_oeuvre=>Oeuvre_Ext.date, prix: Decimal) avec début NOT NULL, fin NOT NULL, prix NOT NULL

+ Prêt(début: Date, fin: Date, #musée=>Musée_Extérieur.nom, #titre_oeuvre=>Oeuvre_Louvre.titre, #date_oeuvre=>Oeuvre_Louvre.date, prix: Decimal) avec début NOT NULL, fin NOT NULL, prix NOT NULL

+ Prestataire(#nom: String, raison_sociale: String)

+ Restauration(#date: Date, type: String, prix: Decimal, prestataire=>Prestataire.nom, #titre_oeuvre=>Oeuvre_Louvre.titre, #date_oeuvre=>Oeuvre_Louvre.date) avec prestataire  NOT NULL, prix NOT NULL

+ Créneau(#jour: {Lundi...Dimanche}, #horaire_début: Integer #exposition_permanante=>Exposition_Permanante.nom)

+ Guide(#id: Integer, nom: String, prénom: String, adresse: JSON, embauche: Date, exposition_temporaire=>Expostion_Temporaire.nom) avec nom  NOT NULL, prénom NOT NULL

+ Créneau_Guide(#guide=>Guide.id, #jour=>Créneau.jour, #horaire_début=>Créneau.horaire_début, #exposition_permanante=>Créneau.exposition_permanante)

+ Salle(#numéro: Integer, capacité: Integer, exposition_temporaire=>Exposition_Temporaire.nom)

+ Panneau(numéro: Integer, #texte: String, salle=>Salle.numéro) avec salle NOT NULL

+ Utilisateur(#login: String, pwd: String, role:{Admin|Membre}) avec role NOT NULL, pwdd NOT NULL

# Contraintes
+ Exposition(Héritage par classe mère, abstraite)  
  Intersection(Projection(Exposition_Permanante,nom), Projection(Exposition_Temporaire,nom)) = {}
+ Oeuvres(Héritage par classe mère, abstraite)  
  Intersection(Projection(Oeuvres_Louvre,titre, date, dimension, deja_empruntée, type_oeuvre), Projection(Oeuvres_Exterieur,titre, date, dimension, deja_empruntée, type_oeuvre)) = {}
+ Date
  fin > début   
  mort > naissance
+ Salle - Exposition_Temporaire   
  Projection(Exposition_Temporaire,nom) ⊆ Projection(Salle,exposition_temporaire)
+ Oeuvre Louvre   
  NOT(Projection(Restauration, titre_oeuvre, date_oeuvre) AND ((Projection(Prêt, titre_oeuvre, date_oeuvre) OR  Projection(Oeuvre_Louvre, titre, date)))


# Vue
+ vExposition = Union(Projection(Exposition_Permanante,nom), Projection(Exposition_Temporaire,nom))
+ vOeuvres = Union(Projection(Oeuvres_Louvre,titre, date, dimension, déja_empruntée), Projection(Oeuvres_Extérieur,titre, date, dimension, déja_empruntée))
+ vRestauration = Jointure(
    JointureNaturelle(Projection(Restauration, date, type, montant), Projection(Prestataire,nom)), 
    Projection(Oeuvre_Louvre, titre, date), 
    Oeuvre_Louvre(titre, date)= Restauration(titre_oeuvre, date_oeuvre)
    )
+ vCréneau = JointureNaturelle(Projection(Créneau, jour, horaire), Projection(Exposition_Permanante, nom))
+ vGuides = JointureNaturelle(Projection(Créneau_Guide, jour, horaire, exposition_permanante), Projection(Guide, nom, prénom, adresse, embauche, exposition_temporaire))
+ vEmprunt = Jointure(
    JointureNaturelle(Projection(Emprunt, début, fin, prix), Projection(Musée_Extérieur,nom)), 
    Projection(Oeuvre_Ext, titre, date), 
    Oeuvre_Ext(titre, date)= Emprunt(titre_oeuvre, date_oeuvre)
    )
+ vPrêt = Jointure(
    JointureNaturelle(Projection(Prêt, début, fin), Projection(Musée_Extérieur,nom)), 
    Projection(Oeuvre_Louvre, titre, date), 
    Oeuvre_Louvre(titre, date)= Prêt(titre_oeuvre, date_oeuvre)
    )
+ vSalle = JointureNaturelle(Projection(Salle, numéro, capacité), Projection(Exposition_Temporaire, nom))
+ vPanneau = JointureNaturelle(Projection(Panneau, numéro, texte), Projection(Salle, numéro))
