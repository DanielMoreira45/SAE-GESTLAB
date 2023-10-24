-- create database if not exists `GestLab` default character set utf8 collate utf8_general_ci;
-- use `GestLab`;


drop table if exists `Commander`;
drop table if exists `Commande`;
drop table if exists `Utilisateur`;
drop table if exists `Role`;
alter table if exists `Contenir` drop foreign key fk_ref_materiel;
alter table if exists `Materiel` drop foreign key fk_date_peremption;
drop table if exists `Materiel`;
drop table if exists `Contenir`;
drop table if exists `Categorie`;
drop table if exists `Domaine`;


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
    codeD int(5),
    nomC varchar(50),
    primary key (codeC, codeD)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Materiel`(
    refMateriel int(5),
    codeD int(5),
    codeC int(5),
    nomMateriel varchar(50),
    precisionMateriel varchar(50),
    commentaire varchar(50),
    qteMateriel float(5),
    unite varchar(25),
    complements varchar(350),
    ficheFDS longblob,
    seuilQte int(5),    -- à environ 25% de la quantité du produit
    seuilPeremption int(5), -- nombre de jours avant la date de péremption
    datePeremption date,
    primary key (refMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Contenir`(
    datePeremption date,
    refMateriel int(5),
    qteDate int(5),
    primary key (datePeremption, refMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Commande`(
    numeroCommande int(5),
    idUti int(5),
    refMateriel int(5),
    dateCommande date,
    dateReception date,
    statut varchar(20),
    primary key (numeroCommande, idUti, refMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Commander`(
    numeroCommande int(5),
    idUti int(5),
    refMateriel int(5),
    qteCommandee int(5),
    primary key (numeroCommande, idUti, refMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;


alter table `Utilisateur` add foreign key (idRole) references `Role`(idRole);
alter table `Categorie` add foreign key (codeD) references `Domaine`(codeD);
alter table `Materiel` add foreign key (codeD) references `Categorie`(codeD);
alter table `Materiel` add foreign key (codeC) references `Categorie`(codeC);
alter table `Materiel` add constraint fk_date_peremption foreign key (datePeremption) references `Contenir`(datePeremption);
alter table `Contenir` add constraint fk_ref_materiel foreign key (refMateriel) references `Materiel`(refMateriel);
alter table `Commande` add foreign key (idUti) references `Utilisateur`(idUti);
alter table `Commande` add foreign key (refMateriel) references `Materiel`(refMateriel);
alter table `Commander` add foreign key (idUti) references `Utilisateur`(idUti);
alter table `Commander` add foreign key (refMateriel) references `Materiel`(refMateriel);
