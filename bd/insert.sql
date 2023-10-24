INSERT INTO Role(idRole, intitule)
VALUES
(1, 'Administrateur'),
(2, 'Professeur'),
(3, 'Etablissement');

INSERT INTO Utilisateur(idUti, idRole, nomUti, prenomUti, emailUti, telUti)
VALUES
(1, 1, 'Doe', 'John', 'johndoe@gmail.com', '0142424242'),
(2, 2, 'Obi', 'Leo', 'leoobi@gmail.com', '0648484848'),
(3, 2, 'Lea', 'Rose', 'roselea@gmail.com', '0162626262'),
(4, 3, 'Jr.', 'Tim', 'timjr@gmail.com', '0142424242'),
(5, 3, 'Zed', 'Zoey', 'zoeyzed@gmail.com', '0142424242');

INSERT INTO Domaine(codeD, nomD)
VALUES
(1, 'Appareillage'),
(2, 'Verrerie et associés'),
(3, 'Produits Chimiques'),
(4, 'Matériel de Laboratoire'),
(5, 'Média'),
(6, 'Matériel Électrique');

INSERT INTO Categorie(codeC, nomC, codeD)
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

INSERT INTO Materiel(refMateriel, nomMateriel, precisionMateriel, commentaire, qteMateriel, unite, complements, ficheFDS, seuilQte, seuilPeremption, datePeremption, codeC, codeD, qteMax)
VALUES
(1, 'Microscope Électronique', 'Armoire 1 Tiroir A', '', 10, null, "observer des échantillons à l'échelle microscopique", null, 2, null, null, 1, 1, 10),
(2, 'Spectrophotomètre', 'Armoire 1 Tiroir A', '', 10, null, "mesure l'absorbance ou la transmission de la lumière", null, 2, null, null, 2, 1, 10),
(3, 'Ordinateur', 'Armoire 1 Tiroir B', '', 50, null, "enregistrer, analyser et afficher les données", null, 2, null, null, 3, 1, 50),
(4, 'Projecteur', 'Armoire 1 Tiroir C', '', 5, null, "donner des présentations et des cours interactifs,", null, 2, null, null, 4, 1, 5),
(5, 'Réacteur Chimique', 'Armoire 1 Tiroir D', '', 10, null, "mener des expériences de synthèse chimique", null, 2, null, null, 5, 1, 10),
(6, 'Gants de sécurité', 'Armoire 1 Tiroir D', 'à laver aprés utilisation', 50, null, "protéger les chercheurs des produits chimiques potentiellement dangereux", null, 2, null, null, 6, 1, 50),
(7, 'Tube à essai', 'Armoire 2 Tiroir A', '', 50, null, "petits tubes en verre", null, 12, null, null, 7, 2, 50),
(8, 'Bécher', 'Armoire 2 Tiroir C', '', 30, null, "récipients cylindriques en verre avec un bord droit", null, 7, null, null, 7, 2, 50),
(9, 'Fiole Conique', 'Armoire 2 Tiroir D', '', 30, null, "mélanger, chauffer, ou contenir des liquides", null, 7, null, null, 7, 2, 50),
(10, 'Acétone', 'Armoire 3 Tiroir A', '', 1000, 'ml', "nettoyer du matériel de laboratoire", null, null, 30, '2023-12-30', 8, 3, 2000),
(11, 'Acide Sulfurique', 'Armoire 3 Tiroir B', '', 1000, 'ml', "la digestion des échantillons et la préparation de solutions réactives", null, null, 30, '2023-12-30', 9, 3, 2000),
(12, 'Amylase', 'Armoire 3 Tiroir C', '', 1000, 'ml', "catalyse la dégradation de l'amidon en sucres plus simples", null, null, 30, '2023-12-30', 10, 3, 2000),
(13, 'Bleu de méthylène', 'Armoire 3 Tiroir D', '', 1000, 'ml', "coloration des cellules", null, null, 30, '2023-12-30', 11, 3, 2000),
(14, 'Solution de détartrage', 'Armoire 3 Tiroir E', '', 500, 'ml', "éliminer les dépôts minéraux", null, null, 125, '2023-12-30', 12, 3, 2000),
(15, 'Silice gel', 'Armoire 3 Tiroir F', '', 1000, 'g', "absorber l'humidité", null, null, 30, '2023-12-30', 13, 3, 2000),
(16, 'Spectrophotomètre UV-Visible', 'Armoire 4 Tiroir A', '', 5, null, "mesurer la transmission de la lumière", null, 2, null, null, 14, 4, 5),
(17, 'Douche de sécurité', 'Salle 1', '', 2, null, "rincer rapidement une personne en cas d'exposition à des produits chimiques dangereux", null, 2, null, null, 15, 4, 5),
(18, 'Pipettes', 'Armoire 4 Tiroir B', '', 30, null, "prélever et transférer des volumes précis de liquides", null, 2, null, null, 16, 4, 50),
(19, 'Hotte chimique', 'Armoire 4 Tiroir C', '', 5, null, "enceinte de sécurité", null, 2, null, null, 17, 4, 10),
(20, 'Gants de laboratoire', 'Armoire 4 Tiroir C', 'à laver aprés utilisation', 50, null, "protéger les mains des chercheurs", null, 2, null, null, 18, 4, 100),
(21, 'ChemDraw', '', '', 1, null, "logiciel de dessin chimique", null, 2, null, null, 19, 5, 1),
(22, 'DVD de formation en sécurité chimique', 'Armoire 5 Tiroir A', '', 5, null, "vidéos explicatives sur les bonnes pratiques de sécurité", null, 2, null, null, 20, 5, 20),
(23, '"Chimie Organique" de Paula Yurkanis Bruice', 'Armoire 5 Tiroir B', '', 15, null, "principes fondamentaux de la chimie organique", null, 2, null, null, 21, 5, 20),
(24, '"Chimie Physique" de Peter Atkins et Julio d Paula', 'Armoire 5 Tiroir B', '', 5, null, "principes fondamentaux de la chimie physique", null, 2, null, null, 22, 5, 20),
(25, 'Tableau périodique', 'Armoire 5 Tiroir C', '', 5, null, "informations sur les éléments chimiques", null, 2, null, null, 23, 5, 50),
(26, 'Articles scientifiques', 'Armoire 5 Tiroir C', '', 5, null, "référence pour la recherche et la littérature scientifique", null, 2, null, null, 24, 5, 50),
(27, 'Alimentation électrique réglable', 'Armoire 6 Tiroir A', '', 5, null, " fournir des courants électriques variables", null, 2, null, null, 25, 6, 10),
(28, 'Multimètre', 'Armoire 6 Tiroir A', '', 15, null, "mesure électrique polyvalent utilisé", null, 2, null, null, 26, 6, 50),
(29, 'Chauffe-ballon', 'Armoire 6 Tiroir B', '', 5, null, "chauffer des réactions chimiques dans un ballon", null, 2, null, null, 27, 6, 10),
(30, 'Câbles de liaison BNC', 'Armoire 6 Tiroir C', '', 5, null, "connecter des instruments de mesure", null, 2, null, null, 28, 6, 10),
(31, 'Fil de platine', 'Armoire 6 Tiroir C', '', 5, 'm', "fabriquer des électrodes et des capteurs électrochimiques", null, 2, null, null, 29, 6, 10),
(32, 'Fusibles électriques', 'Armoire 6 Tiroir C', '', 5, null, "protéger les circuits électriques sensibles", null, 2, null, null, 30, 6, 10),
(33, 'Burette', 'Armoire 2 Tiroir B', '', 50, null, "mesurer précisément le volume d'une solution versée dans une autre", null, 12, null, null, 7, 2, 50);

INSERT INTO Commande(numeroCommande, dateCommande, dateReception, statut, idUti, refMateriel)
VALUES
(1, '2023-10-23', '2023-10-30', 'Livrée', 2, 1),
(2, '2023-10-23', '2023-10-30', 'Livrée', 2, 2),
(3, '2023-10-25', '2023-11-25', 'En cours', 3, 14),
(4, '2023-10-25', '2023-11-25', 'En cours', 2, 18),
(5, '2023-10-27', '2023-11-23', 'En cours', 3, 33);

INSERT INTO Commander(numeroCommande, idUti, refMateriel, qteCommandee)
VALUES
(1, 2, 1, 10),
(2, 2, 2, 10),
(3, 3, 14, 10),
(4, 2, 18, 10),
(5, 3, 33, 10);

INSERT INTO Alerte(idAlerte, refMateriel, commentaire)
VALUES
(1, 25, 'Alerte de quantité'),
(2, 26, 'Alerte de quantité');