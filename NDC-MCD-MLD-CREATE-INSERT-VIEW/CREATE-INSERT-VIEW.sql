-------------- CREATION DE BASE DES DONNEES--------------
CREATE DATABASE louvre WITH OWNER postgres;  -->Erreur, manque du droit

-------------- CREATION DES ROLES -------------- 
    --> Administateur
CREATE ROLE Admin NOSUPERUSER INHERIT CREATEDB CREATEROLE REPLICATION;
    --> Membres d'équipe
CREATE ROLE Membre NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;
    --> Guide
CREATE ROLE Guide NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;
    --> Prestataire
CREATE ROLE Prestataire NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;
    --> Visiteur
CREATE ROLE Visiteur NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;

-------------- CONNECTION A LA BASE -------------- 
GRANT CONNECT ON DATABASE louvre TO Admin;
GRANT CONNECT ON DATABASE louvre TO Membre;
GRANT CONNECT ON DATABASE louvre TO Guide;
GRANT CONNECT ON DATABASE louvre TO Prestataire;
GRANT CONNECT ON DATABASE louvre TO Visiteur;

-------------- GESTION DES DROITS --------------
GRANT ALL PRIVILEGES ON  ALL TABLES IN SCHEMA louvre TO Admin;
REVOKE ALL PRIVILEGES ON Utilisateur IN SCHEMA louvre FROM Membre;
GRANT SELECT, UPDATE, INSERT ON  ALL TABLES IN SCHEMA louvre TO Membre;
GRANT SELECT ON Creneau_Guide IN SCHEMA louvre TO Guide;
GRANT SELECT ON Guide IN SCHEMA louvre TO Guide;
GRANT SELECT, UPDATE, INSERT ON Restauration IN SCHEMA louvre TO Prestataire;
GRANT SELECT ON Exposition_Temporaire IN SCHEMA louvre TO Visiteur;
GRANT SELECT ON Exposition_Permanante IN SCHEMA louvre TO Visiteur;

-------------- INSTANTIATION DES TABLES --------------
-- Supprimer toutes les tables en cas d'existance, car il y a de dépendance parmis les tables, il faut d'abord supprimer la table dépendue par d'autres--
DROP TABLE Emprunt;
DROP TABLE Pret;
DROP TABLE Restauration;
DROP TABLE Creneau_Guide;
DROP TABLE Salle;
DROP TABLE Panneau;
DROP TABLE Utilisateur;
DROP TABLE Prestataire;
DROP TABLE Musee_Exterieur;
DROP TABLE Oeuvre_Louvre;
DROP TABLE Oeuvre_Ext;
DROP TABLE Creneau;
DROP TABLE Guide;
DROP TABLE Auteur;
DROP TABLE Exposition_Permanante;
DROP TABLE Exposition_Temporaire;

-- Musee_Exterieur --
CREATE TABLE Musee_Exterieur(
    nom VARCHAR(50) PRIMARY KEY,
    adresse JSON NOT NULL
);
-- Auteur --
CREATE TABLE Auteur(
    nom VARCHAR(50),
    prenom VARCHAR(50),
    naissance DATE,
    mort DATE,
    CHECK(mort > naissance),
    PRIMARY KEY (nom,prenom,naissance)
);
-- Exposition_Permanante --
CREATE TABLE Exposition_Permanante(
    nom VARCHAR(50) PRIMARY KEY
);
-- Exposition_Temporaire --
CREATE TABLE Exposition_Temporaire(
    nom VARCHAR(50) PRIMARY KEY,
    debut DATE NOT NULL,
    fin DATE NOT NULL,
    CHECK(fin > debut)
);
-- Oeuvre_Louvre --
CREATE TABLE Oeuvre_Louvre(
    titre VARCHAR(50),
    date DATE,
    dimension JSON,
    deja_empruntee BOOLEAN NOT NULL,
    type_oeuvre VARCHAR(50) NOT NULL CHECK (type_oeuvre IN ('Peinture','Sculpture', 'photographies')),
    nom_auteur VARCHAR(50),
    prenom_auteur VARCHAR(50),
    naissance_auteur DATE,
    exposition VARCHAR(50),
    prix DECIMAL NOT NULL,
    PRIMARY KEY(titre, date),
    FOREIGN KEY(nom_auteur,prenom_auteur,naissance_auteur) REFERENCES Auteur(nom,prenom,naissance),
    FOREIGN KEY(exposition) REFERENCES Exposition_Permanante(nom)
);
-- Oeuvre_Ext --
CREATE TABLE Oeuvre_Ext(
    titre VARCHAR(50),
    date DATE,
    dimension JSON,
    deja_empruntee BOOLEAN NOT NULL,
    type_oeuvre VARCHAR(50) NOT NULL CHECK (type_oeuvre IN ('Peinture','Sculpture', 'photographies')),
    nom_auteur VARCHAR(50),
    prenom_auteur VARCHAR(50),
    naissance_auteur DATE,
    exposition VARCHAR(50) NOT NULL,
    PRIMARY KEY(titre, date),
    FOREIGN KEY(nom_auteur,prenom_auteur,naissance_auteur) REFERENCES Auteur(nom,prenom,naissance),
    FOREIGN KEY(exposition) REFERENCES Exposition_Temporaire(nom)
);
-- Emprunt --
CREATE TABLE Emprunt(
    debut DATE NOT NULL,
    fin DATE NOT NULL,
    musee VARCHAR(50),
    titre_oeuvre VARCHAR(50),
    date_oeuvre DATE,
    prix Decimal NOT NULL,
    CHECK(fin > debut),
    PRIMARY KEY(musee, titre_oeuvre, date_oeuvre),
    FOREIGN KEY(musee) REFERENCES Musee_Exterieur(nom),
    FOREIGN KEY(titre_oeuvre,date_oeuvre ) REFERENCES Oeuvre_Ext(titre, date)
);
-- Pret --
CREATE TABLE Pret(
    debut DATE NOT NULL,
    fin DATE NOT NULL,
    musee VARCHAR(50),
    titre_oeuvre VARCHAR(50),
    date_oeuvre DATE,
    prix Decimal NOT NULL,
    CHECK(fin > debut),
    PRIMARY KEY(musee, titre_oeuvre, date_oeuvre),
    FOREIGN KEY(musee) REFERENCES Musee_Exterieur(nom),
    FOREIGN KEY(titre_oeuvre,date_oeuvre ) REFERENCES Oeuvre_Louvre(titre, date)
);
-- Prestataire --
CREATE TABLE Prestataire(
    nom VARCHAR(50) PRIMARY KEY, 
    raison_sociale VARCHAR(50)
);
-- Restauration --
CREATE TABLE Restauration(
    date DATE,
    type VARCHAR(50),
    prix DECIMAL NOT NULL,
    prestataire VARCHAR(50) NOT NULL,
    titre_oeuvre VARCHAR(50),
    date_oeuvre DATE,
    PRIMARY KEY (date, titre_oeuvre, date_oeuvre),
    FOREIGN KEY(prestataire) REFERENCES Prestataire(nom),
    FOREIGN KEY(titre_oeuvre,date_oeuvre) REFERENCES Oeuvre_Louvre(titre, date)
);
-- Creneau --
CREATE TABLE Creneau(
    jour VARCHAR(8) CHECK (jour IN ('Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche')),
    horaire_debut INTEGER,
    exposition_permanante VARCHAR(50),
    PRIMARY KEY (jour,horaire_debut, exposition_permanante),
    FOREIGN KEY(exposition_permanante) REFERENCES Exposition_Permanante(nom)
);
-- Guide --
CREATE TABLE Guide(
    id INTEGER PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    adresse JSON,
    embauche DATE,
    exposition_temporaire VARCHAR(50),
    FOREIGN KEY(exposition_temporaire) REFERENCES Exposition_Temporaire(nom)
);
-- Creneau_Guide --
CREATE TABLE Creneau_Guide(
    guide INTEGER,
    jour VARCHAR(8),
    horaire_debut INTEGER,
    exposition_permanente VARCHAR(50),
    PRIMARY KEY (guide,jour,horaire_debut,exposition_permanente),
    FOREIGN KEY(guide) REFERENCES Guide(id),
    FOREIGN KEY(jour,horaire_debut, exposition_permanente) REFERENCES Creneau(jour,horaire_debut, exposition_permanante),
    UNIQUE (guide, jour, horaire_debut) 
);
-- Salle --
CREATE TABLE Salle(
    numero INTEGER PRIMARY KEY,
    capacite INTEGER,  
    exposition_temporaire VARCHAR(50),
    FOREIGN KEY(exposition_temporaire) REFERENCES Exposition_Temporaire(nom)
);
-- Panneau --
CREATE TABLE Panneau(
    numero INTEGER,
    texte VARCHAR(100) PRIMARY KEY,
    salle INTEGER  NOT NULL REFERENCES Salle(numero)
);
-- Utilisateur pour accéder à l'application--
CREATE TABLE Utilisateur(
    login VARCHAR(50),
    pwd VARCHAR(50) NOT NULL,
    role VARCHAR(50)  NOT NULL CHECK (role IN ('Admin','Membre')),
    PRIMARY KEY (login)
);

-------------- INSERTION DES DONNEES -------------- 
-- Musee_Exterieur --
INSERT INTO Musee_Exterieur VALUES ('Musée d''Orsay', 
'{"numéro":1, "rue":"Rue de la Légion d''Honneur", "cp":"75007", "ville": "Paris"}'
);
INSERT INTO Musee_Exterieur VALUES ('Le Centre Pompidou', 
'{"numéro":3, "rue":"Musée National Picasso-Paris", "cp":"75004", "ville": "Paris"}'
);
INSERT INTO Musee_Exterieur VALUES ('Musée National Picasso-Paris', 
'{"numéro":5, "rue":"Rue de Thorigny", "cp":"75003", "ville": "Paris"}'
);
INSERT INTO Musee_Exterieur VALUES ('Musée de l''Armée', 
'{"numéro":129, "rue":"129 Rue de Grenell", "cp":"75007", "ville": "Paris"}'
);
-- Auteur --
INSERT INTO Auteur VALUES ('Léonard', 'De Vinci', '1452-04-15' ,'1519-05-02');
INSERT INTO Auteur VALUES ('Alexandros', 'D''Antioche', '1003-04-10', '1083-03-11');
INSERT INTO Auteur VALUES ('Eugène', 'Delacroix', '1798-04-26', '1863-08-13');
INSERT INTO Auteur VALUES ('Charles', 'Champoiseau', '1830-05-01', '1909-06-29');
INSERT INTO Auteur VALUES ('Gustave', 'Courbet', '1819-06-10', '1877-12-31');
INSERT INTO Auteur VALUES ('Vincent', 'Van Gogh', '1853-03-30' , '1890-07-29');
INSERT INTO Auteur VALUES ('Henri', 'Matisse', '1869-12-31', '1954-11-03');
INSERT INTO Auteur VALUES ('Otto', 'Dix', '1891-12-02', '1969-07-25');
INSERT INTO Auteur VALUES ('Pablo', 'Picasso', '1881-10-25', '1973-04-08');
-- Exposition_Permanante --
INSERT INTO Exposition_Permanante VALUES ('EP1');
INSERT INTO Exposition_Permanante VALUES ('EP2');
INSERT INTO Exposition_Permanante VALUES ('EP3');
-- Exposition_Temporaire --
INSERT INTO Exposition_Temporaire VALUES ('ET1', '2020-11-26', '2020-12-26');
INSERT INTO Exposition_Temporaire VALUES ('ET2', '2020-11-26', '2020-12-03');
INSERT INTO Exposition_Temporaire VALUES ('ET3', '2020-12-01', '2020-12-25');
INSERT INTO Exposition_Temporaire VALUES ('ET4', '2021-01-01', '2021-02-10');
-- Oeuvre_Louvre --
INSERT INTO Oeuvre_Louvre VALUES ('La Joconde', '1503-11-10', '{"x":53, "y":77, "z":0}', True, 'Peinture', 'Léonard',  'De Vinci', '1452-04-15', 'EP1', 20000);
INSERT INTO Oeuvre_Louvre VALUES ('Vénus de Milo', '1820-07-08', '{"x":130, "y":140, "z":150}', True, 'Sculpture', 'Alexandros', 'D''Antioche', '1003-04-10', 'EP1', 2000);
INSERT INTO Oeuvre_Louvre VALUES ('La Liberté guidant le peuple', '1830-06-12', '{"x":325, "y":260, "z":0}', True, 'Peinture', 'Eugène', 'Delacroix', '1798-04-26', 'EP2', 3000);
INSERT INTO Oeuvre_Louvre VALUES ('Victoire de Samothrace', '1863-03-14', '{"x":130, "y":140, "z":512}', False, 'Sculpture', 'Charles', 'Champoiseau', '1830-05-01', 'EP2', 10000);
-- Oeuvre_Ext --
INSERT INTO Oeuvre_Ext VALUES ('L''Origine du monde', '1866-12-01', '{"x":46, "y":55, "z":0}', True, 'Peinture', 'Gustave', 'Courbet', '1819-06-10', 'ET1');
INSERT INTO Oeuvre_Ext VALUES ('Autoportrait', '1889-09-07', '{"x":65, "y":54, "z":0}', True, 'Peinture', 'Vincent', 'Van Gogh', '1853-03-30', 'ET2');
INSERT INTO Oeuvre_Ext VALUES ('La Nuit étoilée', '1888-12-25', '{"x":72, "y":92, "z":0}', True, 'Peinture', 'Vincent', 'Van Gogh', '1853-03-30', 'ET1');
INSERT INTO Oeuvre_Ext VALUES ('La Tristesse du roi', '1952-10-10', '{"x":292, "y":386, "z":0}', False, 'Peinture', 'Henri', 'Matisse',  '1869-12-31', 'ET3');
INSERT INTO Oeuvre_Ext VALUES ('Portrait de la journaliste Sylvia von Harden', '1926-11-27', '{"x":121, "y":89, "z":0}', False, 'Sculpture', 'Otto', 'Dix', '1891-12-02', 'ET4');
INSERT INTO Oeuvre_Ext VALUES ('La Mort de Casagemas', '1901-02-24', '{"x":27, "y":35 , "z":0}', False, 'Peinture', 'Pablo', 'Picasso', '1881-10-25', 'ET3');
INSERT INTO Oeuvre_Ext VALUES ('La fille aux pieds nus', '1895-05-15', '{"x":75, "y":50, "z":0}', False, 'Peinture', 'Pablo', 'Picasso', '1881-10-25', 'ET3');
-- Emprunt --
INSERT INTO Emprunt VALUES ('2020-11-30', '2020-12-15', 'Musée d''Orsay', 'L''Origine du monde', '1866-12-01', 500);
INSERT INTO Emprunt VALUES ('2020-11-30', '2020-12-15', 'Musée d''Orsay', 'Autoportrait', '1889-09-07',  500);
INSERT INTO Emprunt VALUES ('2020-12-23', '2021-02-27', 'Le Centre Pompidou', 'La Nuit étoilée', '1888-12-25', 600);
-- Prêt --
INSERT INTO Pret VALUES ('2020-11-18', '2020-12-15', 'Musée d''Orsay', 'La Joconde', '1503-11-10', 20000);
INSERT INTO Pret VALUES ('2020-11-18', '2020-12-15', 'Musée d''Orsay', 'Vénus de Milo', '1820-07-08', 2000);
INSERT INTO Pret VALUES ('2020-12-30', '2021-02-14', 'Le Centre Pompidou', 'Vénus de Milo', '1820-07-08', 2000);
INSERT INTO Pret VALUES ('2020-12-30', '2021-02-14', 'Le Centre Pompidou',  'La Liberté guidant le peuple', '1830-06-12', 3000);
-- Prestataire --
INSERT INTO Prestataire VALUES ('Paul', 'SASU');
INSERT INTO Prestataire VALUES ('Yann', 'EURL');
INSERT INTO Prestataire VALUES ('Juliette', 'SAS');
INSERT INTO Prestataire VALUES ('Camille', 'SARL');
INSERT INTO Prestataire VALUES ('Maxime', 'SNC');
INSERT INTO Prestataire VALUES ('Bastien', 'SA');
-- Restauration --
INSERT INTO Restauration VALUES ('2020-11-20', 'Léger' , 20000, 'Paul', 'La Joconde', '1503-11-10');
-- Creneau --
INSERT INTO Creneau VALUES ('Lundi', 9, 'EP1');
INSERT INTO Creneau VALUES ('Lundi', 9, 'EP2');
INSERT INTO Creneau VALUES ('Mardi', 11, 'EP1');
INSERT INTO Creneau VALUES ('Vendredi', 10, 'EP1');
INSERT INTO Creneau VALUES ('Vendredi', 13, 'EP3');
-- Guide --
INSERT INTO Guide VALUES (1, 'Adlan', 'MERLO', '{"numéro":3, "rue":"Rue de la Légion d''Honneur", "cp":"60200", "ville": "Compiègne"}', '2018-11-10', 'ET1');
INSERT INTO Guide VALUES (2, 'Alain', 'Donadey', '{"numéro":35, "rue":"Musée National Picasso", "cp":"69006", "ville": "Lyon"}', '2019-02-17', 'ET1');
INSERT INTO Guide VALUES (3, 'Anais', 'Schumacher', '{"numéro":13, "rue":"Musée National", "cp":"60200", "ville": "Compiègne"}', '2015-03-15', 'ET1');
INSERT INTO Guide VALUES (4, 'Anne', 'MEULEAU', '{"numéro":35, "rue":"Rue de Grenell", "cp":"75007", "ville": "Paris"}', '2015-03-15',  'ET2');
-- Creneau_Guide --
INSERT INTO Creneau_Guide VALUES (1, 'Lundi', 9, 'EP1');
INSERT INTO Creneau_Guide VALUES (2, 'Lundi', 9, 'EP1');
INSERT INTO Creneau_Guide VALUES (2, 'Mardi', 11, 'EP1');
-- Salle --
INSERT INTO Salle VALUES (1, 500, 'ET1');
INSERT INTO Salle VALUES (2, 300, 'ET1');
INSERT INTO Salle VALUES (3, 500, 'ET2');
-- Panneau --
INSERT INTO Panneau VALUES (1, 'Panneau1', 1);
INSERT INTO Panneau VALUES (2, 'Panneau2', 2);
-- Utilisateur pour accéder à l'application--
INSERT INTO Utilisateur VALUES ('Jinshan GUO', 'nf18', 'Admin');
INSERT INTO Utilisateur VALUES ('Qi XIA', 'nf18', 'Membre');
INSERT INTO Utilisateur VALUES ('Jules YVON', 'nf18', 'Membre');
INSERT INTO Utilisateur VALUES ('Batien LE CALVE', 'nf18', 'Membre');
INSERT INTO Utilisateur VALUES ('Alessandro Correa-Victorino', 'nf18', 'Membre');

-------------- VUES PRINCIPALES --------------
-- Vérifier la contrainte d'héritage de classe 'Exposition' 
CREATE VIEW vExposition (Nom) AS
SELECT nom FROM Exposition_Permanante
UNION  
SELECT nom FROM Exposition_Temporaire 
ORDER BY nom;
    --  Afficher le résultat
SELECT * FROM vExposition;

-- Vérifier la contrainte d'héritage de classe 'Oeuvres'
    --  Vue Oeuvre Louvre
CREATE VIEW vOeuvreLouvre (Titre, Date_oeuvre, X, Y, Z, Deja_empruntee, Type_oeuvre, Auteur_nom, Auteur_prenom, Auteur_naissance, Exposition, Prix) AS 
SELECT titre, date,  CAST(dimension->>'x' AS INTEGER), CAST(dimension->>'y' AS INTEGER), CAST(dimension->>'z' AS INTEGER), deja_empruntee, type_oeuvre, nom_auteur, prenom_auteur, naissance_auteur, exposition, prix FROM Oeuvre_Louvre;
	--  Vue Oeuvre Extérieure
CREATE VIEW vOeuvreExt (Titre, Date_oeuvre, X, Y, Z, Deja_empruntee, Type_oeuvre, Auteur_nom, Auteur_prenom, Auteur_naissance, Exposition) AS
SELECT titre, date,  CAST(dimension->>'x' AS INTEGER) AS X, CAST(dimension->>'y' AS INTEGER) AS Y, CAST(dimension->>'z' AS INTEGER) AS Z, deja_empruntee, type_oeuvre, nom_auteur, prenom_auteur, naissance_auteur, exposition FROM Oeuvre_Ext;
    --  Vue Oeuvre Louvre et Extérieure - Vérifier toutes les oeuvres sont différentes
CREATE VIEW vOeuvre (Titre, Date_oeuvre, Type_oeuvre) AS 
SELECT Titre, Date_oeuvre, Type_oeuvre FROM vOeuvreLouvre
UNION
SELECT Titre, Date_oeuvre, Type_oeuvre FROM vOeuvreExt;
	--  Afficher le résultat
-- SELECT * FROM vOeuvre;

-- Vérifier la contrainte 'Une oeuvre en restauration ne peut être ni empruntée ni exposée'
    --  Vue Oeuvre Louvre en restauration
CREATE VIEW vOeuvreLouvreEnRestau (Titre, Date_oeuvre, Prestataire, Date_restau, Type, Prix) AS
SELECT titre_oeuvre, date_oeuvre, prestataire, date, type, prix   
FROM Restauration R;
    --  Afficher le résultat
SELECT * FROM vOeuvreLouvreEnRestau;

    --  Vue Oeuvre Louvre disponible
CREATE VIEW vOeuvreLouvreDispo(Titre, Date_oeuvre) AS
SELECT Titre, Date_oeuvre FROM vOeuvreLouvre WHERE deja_empruntee IS False
EXCEPT
SELECT Titre, Date_oeuvre FROM vOeuvreLouvreEnRestau;
    --  Afficher le résultat
SELECT * FROM vOeuvreLouvreDispo;

-- Vérifier la contrainte 'le prêt d'une œuvre entre le Louvre et un musée extérieur (dans un sens ou dans l'autre) ne peut avoir lieu qu'une seule fois'
    --  Vue Oeuvre déjà prêtée
CREATE VIEW vOeuvreDejaPretee (Titre, Date_oeuvre, Musee, Debut, Fin, Prix) AS   
SELECT titre_oeuvre, date_oeuvre, musee, debut, fin, prix  
FROM Pret;
    --  Vue Oeuvre déjà empruntée
CREATE VIEW vOeuvreDejaEmpruntee (Titre, Date_oeuvre, Musee, Debut, Fin, Prix) AS   
SELECT titre_oeuvre, date_oeuvre, musee, debut, fin, prix  
FROM Emprunt;
    --  Vue Oeuvre ne pouvant être plus prêtée ou empruntée
CREATE VIEW vOeuvresDejaEchangee(Titre, Date_oeuvre, Musee, Debut, Fin, Prix) AS
SELECT * FROM vOeuvreDejaPretee
UNION
SELECT * FROM vOeuvreDejaEmpruntee;
    --  Afficher le résultat
SELECT * FROM vOeuvresDejaEchangee;

 --  Vue Creneau et Creneau_Guide: calculer l'horaire complet en fonction de horaire du début donné
     --  Vue Creneau
CREATE VIEW vCreneau (Jour, Horaire, Exposition) AS   
SELECT jour, CONCAT(horaire_debut, 'h - ', horaire_debut + 2, 'h')AS horaire, exposition_permanante   
FROM Creneau;
    --  Vue Creneau_Guide
CREATE VIEW vCreneauGuide (Guide, Jour, Horaire, Exposition) AS   
SELECT guide, jour, CONCAT(horaire_debut, 'h - ', horaire_debut + 2, 'h') AS horaire, exposition_permanente
FROM Creneau_Guide; 
    --  Afficher le résultat
SELECT * FROM vCreneau;
SELECT * FROM vCreneauGuide;

-- Mettre à jour l'état de l'oeuvre(La meilleure façon est de créer un fonction, ici c'est juste pour indiquer qu'il faut mettre à jour l'état d'emprunt d'oeuvre après avoir été empruntée ou prêtée)
    --  Vue Oeuvre Louvre à mettre à jour
CREATE VIEW vOeuvreLouvreAMettreAJour (Titre, Date_oeuvre, Musee) AS
SELECT OL.titre, OL.date, P.musee 
FROM  Oeuvre_Louvre OL LEFT JOIN Pret P ON OL.titre=P.titre_oeuvre AND OL.date=P.date_oeuvre 
WHERE OL.deja_empruntee=False AND P.musee IS NOT NULL;
    --  Vue Oeuvre Ext à mettre à jour
CREATE VIEW vOeuvreExtAMettreAJour (Titre, Date_oeuvre, Musee) AS
SELECT OE.titre, OE.date, E.musee 
FROM  Oeuvre_Ext OE LEFT JOIN Emprunt E ON OE.titre=E.titre_oeuvre AND OE.date=E.date_oeuvre 
WHERE OE.deja_empruntee=False AND E.musee IS NOT NULL;
    --  Afficher le résultat
SELECT * FROM vOeuvreLouvreAMettreAJour;
SELECT * FROM vOeuvreExtAMettreAJour;

-------------- VUES DES FONCTONS STATISTIQUES -------------- 
--  Calculer le montant des restaurations
CREATE VIEW vMontantRestau (Montant) AS  
SELECT SUM(prix) FROM vOeuvreLouvreEnRestau;
    --  Afficher le résultat
SELECT * FROM vMontantRestau;

--  Calculer le prix moyen des emprunts pour chaque musée
CREATE VIEW vEmpruntMoyen(Musee, Prix_Moyen) AS  
SELECT musee, AVG(prix) AS Moyen FROM vOeuvreDejaEmpruntee GROUP BY musee ORDER BY Moyen DESC;
    --  Afficher le résultat
SELECT * FROM vEmpruntMoyen;

--  Calculer le montant du prix des prets pour chaque musée
CREATE VIEW vMontantPret(Musee, Montant) AS  
SELECT musee, SUM(prix) FROM vOeuvreDejaPretee GROUP BY musee ORDER BY prix DESC;
    --  Afficher le résultat
SELECT * FROM vMontantPret;

--  Calculer la durée des expositions temporaires
CREATE VIEW vDureeExpoTemp(Expostion, Duree_Par_Jour) AS  
SELECT nom, fin-debut FROM Exposition_Temporaire;
    --  Afficher le résultat
SELECT * FROM vDureeExpoTemp;

--  Calculer le prix moyen d'acquisition des oeuvres d'une exposition
CREATE VIEW vPrixMoyenAcqui(Exposition, Prix_Moyen) AS
SELECT exposition, AVG(prix) AS Moyen FROM Oeuvre_Louvre GROUP BY exposition ORDER BY Moyen DESC;
    --  Afficher le résultat
SELECT * FROM vPrixMoyenAcqui;

--  Calculer le temps moyen des prêts avec les musées extérieur
CREATE VIEW vTempsMoyenPrets(Musee, Temps_Moyen) AS
SELECT musee, AVG(fin-debut) AS Temps_Moyen FROM vOeuvreDejaPretee GROUP BY musee ORDER BY Temps_Moyen  DESC;
    --  Afficher le résultat
SELECT * FROM vTempsMoyenPrets;