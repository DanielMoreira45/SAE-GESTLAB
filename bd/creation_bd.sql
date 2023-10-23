-- create database if not exists `GestLab` default character set utf8 collate utf8_general_ci;
-- use `GestLab`;

drop table if exists `Posseder`;
drop table if exists `Contenir`;
drop table if exists `Commander`;
drop table if exists `Commande`;
drop table if exists `Utilisateur`;
drop table if exists `Materiel`;
drop table if exists `Domaine`;
drop table if exists `Categorie`;
drop table if exists `Role`;


create table `Role`(
    idRole int(5),
    intitule varchar(50),
    primary key (idRole)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Utilisateur`(
    idUti int(5),
    idRole int(5),
    nomUti varchar(50),
    prenomUti varchar(50),
    emailUti varchar(50),
    telUti varchar(50),
    primary key (idUti)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Domaine`(
    codeD int(5),
    nomD varchar(50),
    primary key (codeD)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Categorie`(
    codeC int(5),
    nomC varchar(50),
    primary key (codeC)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Materiel`(
    idMateriel int(5),
    codeD int(5),
    codeC int(5),
    nomMateriel varchar(50),
    ficheFDS longblob,
    qteTotale int(5),
    seuilQte int(5),
    seuilPeremption date,
    datePeremption date,
    primary key (idMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Posseder`(
    idUti int(5),
    idMateriel int(5),
    `date` date,
    duree time,
    primary key (idUti, idMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Contenir`(
    datePeremption date,
    idMateriel int(5),
    qteDate int(5),
    primary key (datePeremption, idMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Commande`(
    numeroCommande int(5),
    idUti int(5),
    idMateriel int(5),
    dateCommande date,
    statut varchar(20),
    primary key (numeroCommande, idUti, idMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Commander`(
    numeroCommande int(5),
    idUti int(5),
    idMateriel int(5),
    qteCommandee int(5),
    primary key (numeroCommande, idUti, idMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;


alter table `Utilisateur` add foreign key (idRole) references `Role`(idRole);
alter table `Materiel` add foreign key (codeD) references `Domaine`(codeD);
alter table `Materiel` add foreign key (codeC) references `Categorie`(codeC);
alter table `Materiel` add foreign key (datePeremption) references `Contenir`(datePeremption);
alter table `Posseder` add foreign key (idUti) references `Utilisateur`(idUti);
alter table `Posseder` add foreign key (idMateriel) references `Materiel`(idMateriel);
alter table `Commande` add foreign key (idUti) references `Utilisateur`(idUti);
alter table `Commande` add foreign key (idMateriel) references `Materiel`(idMateriel);
