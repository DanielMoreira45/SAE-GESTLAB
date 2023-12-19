INSERT INTO ROLE(idRole, intitule)
VALUES
(1, 'Administrateur'),
(2, 'Professeur'),
(3, 'Etablissement');

insert into STATUT(idStatut, nomStatut) values
(1, 'Livrée'),
(2, 'En cours'),
(3, 'A valider'),
(4, 'Non validée');

INSERT INTO UTILISATEUR(idUti, idRole, nomUti, prenomUti, emailUti, mdp, modifications)
VALUES
(1, 1, 'Doe', 'John', 'johndoe@gmail.com', 'admin', 1),
(2, 2, 'Obi', 'Leo', 'leoobi@gmail.com', 'Password', 1),
(3, 2, 'Lea', 'Rose', 'roselea@gmail.com', 'Jai', 0),
(4, 3, 'Jr.', 'Tim', 'timjr@gmail.com', '1234', 0),
(5, 3, 'Zed', 'Zoey', 'zoeyzed@gmail.com', 'Dalaigre', 1);

INSERT INTO DOMAINE(codeD, nomD)
VALUES
(1, 'Appareillage'),
(2, 'Verrerie et associés'),
(3, 'Produits Chimiques'),
(4, 'Matériel de Laboratoire'),
(5, 'Média'),
(6, 'Matériel Électrique');

INSERT INTO CATEGORIE(codeC, nomC, codeD)
VALUES
(1, 'Observation', 1),
(2, 'Mesures', 1),
(3, 'ExAO', 1),
(4, 'Multimédia', 1),
(5, 'Expérimentation', 1),
(6, 'Divers', 1),
(7, 'Verrerie', 2),
(8, 'Produits Organiques', 3),
(9, 'Produits Minéraux', 3),
(10, 'Enzymes', 3),
(11, 'Colorants', 3),
(12, 'Entretien', 3),
(13, 'Autres', 3),
(14, 'Appareils de labo', 4),
(15, 'Sécurité', 4),
(16, 'Fournitures', 4),
(17, 'Mobilier', 4),
(18, 'Divers', 4),
(19, 'Logiciels', 5),
(20, 'DVD/VHS', 5),
(21, 'Manuels Scolaires', 5),
(22, 'Livres Scientifiques', 5),
(23, 'Cartes/Posters', 5),
(24, 'Divers', 5),
(25, 'Générateurs', 6),
(26, 'Mesures', 6),
(27, 'Récepteurs', 6),
(28, 'Connectique', 6),
(29, 'Métaux', 6),
(30, 'Divers', 6);

insert into MATERIELGENERIQUE(refMateriel, codeD, codeC, nomMateriel, rangement, commentaire, qteMateriel, qteMax, unite, complements, ficheFDS, seuilQte, seuilPeremption, imageMateriel) values 
(1, 1, 1, 'Microscope Électronique', 'Armoire 1 Tiroir A', 'Voici le commentaire', 10, 10, null, "observer des échantillons à l'échelle microscopique", null, 2, null, null),
(2, 1, 2, 'Spectrophotomètre', 'Armoire 1 Tiroir A', '', 10, 10, null, "mesure l'absorbance ou la transmission de la lumière", null, 2, null, null),
(3, 1, 3, 'Ordinateur', 'Armoire 1 Tiroir B', '', 50, 50, null, "enregistrer, analyser et afficher les données", null, 2, null, null),
(4, 1, 4, 'Projecteur', 'Armoire 1 Tiroir C', '', 5, 5, null, "donner des présentations et des cours interactifs", null, 2, null, null),
(5, 1, 5, 'Réacteur Chimique', 'Armoire 1 Tiroir D', '', 10, 10, null, "mener des expériences de synthèse chimique", null, 2, null, null),
(6, 1, 6, 'Gants de sécurité', 'Armoire 1 Tiroir D', 'à laver après utilisation', 50, 50, null, "protéger les chercheurs des produits chimiques potentiellement dangereux", null, 2, null, null),
(7, 1, 7, 'Tube à essai', 'Armoire 2 Tiroir A', '', 50, 50, null, "petits tubes en verre", null, 12, null, null),
(8, 2, 7, 'Bécher', 'Armoire 2 Tiroir C', '', 30, 50, null, "récipients cylindriques en verre avec un bord droit", null, 7, null, null),
(9, 2, 7, 'Fiole Conique', 'Armoire 2 Tiroir D', '', 30, 50, null, "mélanger, chauffer, ou contenir des liquides", null, 7, null, null),
(10, 3, 8, 'Acétone', 'Armoire 3 Tiroir A', '', 1000, 2000, 'mL', "nettoyer du matériel de laboratoire", null, null, 30, null),
(11, 3, 9, 'Acide Sulfurique', 'Armoire 3 Tiroir B', '', 1000, 2000, 'mL', "la digestion des échantillons et la préparation de solutions réactives", null, null, 30, null),
(12, 3, 10, 'Amylase', 'Armoire 3 Tiroir C', '', 1000, 2000, 'mL', "catalyse la dégradation de l'amidon en sucres plus simples", null, null, 30, null),
(13, 3, 11, 'Bleu de méthylène', 'Armoire 3 Tiroir D', '', 1000, 2000, 'mL', "coloration des cellules", null, null, 30, null),
(14, 3, 12, 'Solution de détartrage', 'Armoire 3 Tiroir E', '', 500, 2000, 'mL', "éliminer les dépôts minéraux", null, null, 125, null),
(15, 3, 13, 'Silice gel', 'Armoire 3 Tiroir F', '', 1000, 2000, 'g', "absorber l'humidité", null, null, 30, null),
(16, 5, 4, 'Spectrophotomètre UV-Visible', 'Armoire 4 Tiroir A', '', 5, 5, null, "mesurer la transmission de la lumière", null, 2, null, null),
(17, 5, 4, 'Douche de sécurité', 'Salle 1', '', 2, 5, null, "rincer rapidement une personne en cas d'exposition à des produits chimiques dangereux", null, 2, null, null),
(18, 4, 16, 'Pipettes', 'Armoire 4 Tiroir B', '', 30, 50, null, "prélever et transférer des volumes précis de liquides", null, 2, null, null),
(19, 4, 17, 'Hotte chimique', 'Armoire 4 Tiroir C', '', 5, 10, null, "enceinte de sécurité", null, 2, null, null),
(20, 4, 18, 'Gants de laboratoire', 'Armoire 4 Tiroir C', 'à laver après utilisation', 50, 100, null, "protéger les mains des chercheurs", null, 2, null, null),
(21, 5, 19, 'ChemDraw', '', '', 1, 1, null, "logiciel de dessin chimique", null, 2, null, null),
(22, 5, 20, 'DVD de formation en sécurité chimique', 'Armoire 5 Tiroir A', '', 5, 20,  null, "vidéos explicatives sur les bonnes pratiques de sécurité", null, 2, null, null),
(23, 5, 21, '"Chimie Organique" de Paula Yurkanis Bruice', 'Armoire 5 Tiroir B', '', 15, 20, null, "principes fondamentaux de la chimie organique", null, 2, null, null),
(24, 5, 22, '"Chimie Physique" de Peter Atkins et Julio d Paula', 'Armoire 5 Tiroir B', '', 5, 20, null, "principes fondamentaux de la chimie physique", null, 2, null, null),
(25, 5, 23, 'Tableau périodique', 'Armoire 5 Tiroir C', '', 5, 50, null, "informations sur les éléments chimiques", null, 2, null, null),
(26, 5, 24, 'Articles scientifiques', 'Armoire 5 Tiroir C', '', 5, 50, null, "référence pour la recherche et la littérature scientifique", null, 2, null, null),
(27, 6, 25, 'Alimentation électrique réglable', 'Armoire 6 Tiroir A', '', 5, 10, null, "fournir des courants électriques variables", null, 2, null, null),
(28, 6, 26, 'Multimètre', 'Armoire 6 Tiroir A', '', 15, 50, null, "mesure électrique polyvalent utilisé", null, 2, null, null),
(29, 6, 27, 'Chauffe-ballon', 'Armoire 6 Tiroir B', '', 5, 10, null, "chauffer des réactions chimiques dans un ballon", null, 2, null, null),
(30, 6, 28, 'Câbles de liaison BNC', 'Armoire 6 Tiroir C', '', 5, 10, null, "connecter des instruments de mesure", null, 2, null, null),
(31, 6, 29, 'Fil de platine', 'Armoire 6 Tiroir C', '', 5, 10, 'm', "fabriquer des électrodes et des capteurs électrochimiques", null, 2, null, null),
(32, 6, 30, 'Fusibles électriques', 'Armoire 6 Tiroir C', '', 5, 10, null, "protéger les circuits électriques sensibles", null, 2, null, null),
(33, 2, 7, 'Burette', 'Armoire 2 Tiroir B', '', 50, 50, null, "mesurer précisément le volume d'une solution versée dans une autre", null, 12, null, null);

insert into MATERIELINSTANCE(idMateriel, qteRestante, datePeremption, refMateriel) values
(1, 1000, '2023-12-30', 10),
(2, 1000, '2023-12-30', 11),
(3, 1000, '2023-12-30', 12),
(4, 1000, '2023-12-30', 13),
(5, 500, '2023-12-30', 14),
(6, 1000, '2023-12-30', 15);

INSERT INTO COMMANDE(numeroCommande, dateCommande, dateReception, qteCommandee, idStatut, idUti, refMateriel)
VALUES
(1, '2023-10-23', '2023-10-30', 2, 1, 2, 1),
(2, '2023-10-23', '2023-10-30', 3, 1, 2, 2),
(3, '2023-10-25', '2023-11-25', 1, 2, 3, 14),
(4, '2023-10-25', '2023-11-25', 6, 2, 2, 18),
(5, '2023-10-27', '2023-11-23', 8, 2, 3, 33),
(6, '2023-11-24', '2023-11-24', 15, 3, 2, 32);

INSERT INTO COMMANDER(numCommande, idUti, refMateriel, qteCommandee)
VALUES
(1, 2, 1, 10),
(2, 2, 2, 10),
(3, 3, 14, 10),
(4, 2, 18, 10),
(5, 3, 33, 10);

INSERT INTO ALERTEQUANTITE(idAlerteQ, refMateriel, commentaire)
VALUES
(1, 25, 'Alerte de quantité'),
(2, 26, 'Alerte de quantité');

insert into ALERTESEUIL(idAlerteS, idMateriel, commentaire) values
(1, 3, 'Alerte : Seuil de peremption atteint'),
(2, 6, 'Alerte : Seuil de peremption atteint');