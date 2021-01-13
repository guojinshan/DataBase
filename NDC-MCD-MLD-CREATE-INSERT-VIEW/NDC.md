# Description
La Note de Clarification(NCD) est une reformulation du cahier des charges, qui précise, ajoute et supprime des éléments (en justifiant) de base de données après l'analyse de la situation existante et des besoins.  
On se focalisera sur l'explicitation des points suivants :  
+ Liste des objets qui devront être gérés dans la base de données
+ Liste des propriétés associées à chaque objet
+ Liste des contraintes associées à ces objets et propriétés
+ Liste des utilisateurs (rôles) appelés à modifier et consulter les données
+ Liste des fonctions que ces utilisateurs pourront effectuer


# Objets

>## Musée Extérieur
>>### Attributs
>>>- nom: String, Unique
>>>- adresse: String

>## Oeuvre (classe abstraite)
>>### Attributs
>>>- titre: String,Unique
>>>- date: Date
>>>- dimension_x: Decimal
>>>- dimension_y: Decimal
>>>- dimension_z: Decimal
>>>- déjà_empruntée: Boolean
>>### Associations
>>>- Chaque oeuvre doit être associée à un type et un auteur.
>>>- La cadinalité entre 'Oeuvre' et 'Type d'oeuvre' est N...1
>>>- La cadinalité entre 'Oeuvre' et 'Auteur' est N...1
>>### Héritages
>>>- Classe-mère de l'Oeuvre Louvre et l'Oeuvre Extérieur.
>>>- Héritage par la classe fille.

>## Type d'oeuvre
>>### Attributs
>>>- type: enum {'Peinture','Sculpture','Photographie'}, Unique  

>## Auteur
>>### Attributs
>>>- nom: String
>>>- prenom: String
>>>- naissance: Date 
>>>- mort: Date
>>### Contraintes
>>>- Le triplet (nom, prenom, naissance) est unique.
>>>- Vérifier mort > naissance.
>## Musée Extérieur
>>### Attributs
>>>- nom: String,Unique
>>>- adresse: String

>## Emprunter  
>>### Attributs
>>>- début: Date
>>>- fin: Date
>>>- prix: Decimal
>>### Contraintes
>>>- Vérifier fin > début.
>>### Associations
>>>- Chaque emprunt concerne un musée extérieur, et une oeuvre extérieure qui n'a pas déjà été empruntée.
>>>- La cadinalité entre 'Emprunter' et 'Musée Extérieur' est N...1
>>>- La cadinalité entre 'Emprunter' et 'Oeuvre Extérieure' est 0,1...1

>## Prêter
>>### Attributs
>>>- début: Date
>>>- fin: Date
>>>- prix: Decimal
>>### Contraintes
>>>- Vérifier fin > début.
>>### Associations
>>>- Chaque prête concerne un musée extérieur, et une oeuvre louvre qui n'a pas déjà été prêtée.
>>>- La cadinalité entre 'Prêter' et 'Musées Extérieurs' est N...1
>>>- La cadinalité entre 'Prêter' et 'Oeuvres Louvre' est 0,1...1

>## Oeuvre Louvre
>>### Attributs
>>>- prix_acquisition: Decimal
>>### Associations
>>>- Une oeuvre Louvre peut être exposée dans une exposition permanente.  
>>>- Une oeuvre Louvre peut être en restauration.
>>>- La cadinalité entre 'Oeuvre Louvre' et 'Exposition Permanante' est N...0,1
>>### Contraintes
>>>-Lorsqu'une oeuvre est en restauration, elle ne peut être ni empruntée ni exposée.

>## Oeuvre Extérieure
>>### Associations
>>>- Une oeuvre extérieure peut être exposée dans une exposition temporaire.  
>>>- La cadinalité entre 'Oeuvre Extérieure' et 'Exposition Temporaire' est N...1

>## Prestataire
>>### Attributs
>>>- nom: String, Unique
>>>- raison_sociale: String

>## Restauration
>>### Attributs
>>>- type: String
>>>- date: Date
>>>- montant: Decimal
>>### Associations
>>>- Une oeuvre louvre peut être réstaurée.
>>>- Chaque restauration est réalisée par un prestataire.
>>>- La cadinalité entre 'Restauration' et 'Oeuvre Louvre' est 0,1...1
>>>- La cadinalité entre 'Restauration' et 'Prestataire' est N...1
>>### Contraintes
>>>- Le couple (Oeuvre Louvre, date) est unique.

>## Exposition (Classe abstraite)
>>### Attributs
>>>- nom: String, Unique
>>### Héritages
>>>- Classe-mère de l'exposition temporaire et l'exposition permanente.
>>>- Héritage par classe fille.

>## Exposition Permanante

>## Exposition Temporaire
>>### Attributs
>>>- début: Date
>>>- fin: Date
>>### Contraintes
>>>- Vérifier fin > début.

>## Créneaux
>>### Attributs
>>>- jour: enum {'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche'}
>>>- horaire: Integer
>>### Associations
>>>- Un créneau concerne une exposition permanente, et n guide(s).
>>>- La cadinalité entre 'Créneaux' et 'Exposition Permanante' est N...1
>>>- La cadinalité entre 'Créneaux' et 'Guide' est N...N
>>### Contraintes
>>>- Le triplet {jour; horaire; permanente} est unique.

>## Guide
>>### Attributs
>>>- id: Integer, Unique 
>>>- nom: String
>>>- prénom: String
>>>- adresse: String
>>>- embauche: Date
>>### Associations
>>>- Un guide peut participer plusieurs expositions permanentes à des créneaux différents.
>>>- Un guide peut être aussi affecté aux expositions temporaires sans créneau indiqué.
>>>- La cadinalité entre 'Guide' et 'Exposition Temporaire' est N...0,1
>>>- La cadinalité entre 'Guide' et 'Créneaux' est N...N
>>### Contraintes 
>>>- Un guide ne peut pas avoir plusieurs créneaux en même temps.
>>>- Un guide affecté à une exposition temporaire ne peut avoir de créneaux (et réciproquement).

>## Salle
>>### Attributs
>>>- numéro: Integer, Unique
>>>- capacité: Integer
>>### Asscociations
>>>- Une salle est dédiée à une exposition temporaire.
>>>- La cadinalité entre 'Salle' et 'Exposition temporaire' est N...1

>## Panneau explicatif
>>### Attributs
>>>- numéro: Integer, Unique
>>>- texte: String
>>### Associations
>>>- Un panneau explicatif est situé dans une des salles de l'exposition.
>>>- La cadinalité entre 'Panneau explicatif' et 'salle' est N...1

># Rôles et privilégiés
>## Administrateur du Louvre
>>- Création, consultation, modification et suppression des informations des ouvres, des expositions, des guides.
>## Guide
>>- Consultation des expositions permanentes affectées et les créneaux associés.
>>- Consultation des expositions temporaire affectées.
>## Prestataire
>>- Consultation de l'enregistrement de réstaurations.
>## Visiteur
>>- Consultation de l'horaire et les oeuvres exposées dans l'exposition.

># Requêtes statistiques
>>- Calculer le prix moyen d'acquisition des œuvre d'une exposition.
>>- Calculer le temps moyen des prêts du Louvre avec les musées extérieurs.
>>- Calculer le temps moyen du travail d'un guide par semaine/mois/an.
>>- Calculer le nombre total de l'oeuvre en restauration.
>>- Calculer le total/moyen/max de nombre de l'oeuvre prêtée aux musées extérieurs par semaine/mois/an.
>>- Calculer le total/moyen/max de nombre de l'oeuvre empruntée des musées extérieurs par semaine/mois/an.
>>- Calculer le nombre des oeuvres total pour chaque auteur.

># View
>>- vOeuvres: afficher toutes les oeuvres gérées.
>>- vExpositions: afficher toutes les expositions gérées.
>>- vRestaurations: afficher toutes les restaurations gérées. 
>>- vCréneaux: afficher tous les créneaux, en plus guides et expositions permanentes asscociées.
>>- vGuides: afficher tous les guides gérés.
>>- vPrêt: afficher toutes les oeuvres prêtées aux musées exrérieures.
>>- vEmprunt:  afficher toutes les oeuvres empruntées des musées exrérieures.
>>- vSalle: afficher toutes les salles gérées.
>>- vPanneaux: afficher tous les panneaux gérés.
(Expression algèbre relationnelle précisé dans le fichier MLD.md)

># Hypothèses et remarques utiles
>>- les expositions gérées sont celles du Louvre et pas celles des musées extérieurs.
>>- le Louvre gère les guides effectuant les visites des expositions.

