-- create database if not exists `GestLab` default character set utf8 collate utf8_general_ci;
-- use `GestLab`;


drop table if exists `Commander`;
drop table if exists `Commande`;
drop table if exists `Utilisateur`;
drop table if exists `Role`;
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
    datePeremption date,
    seuilQte int(5),    -- à environ 25% de la quantité du produit
    seuilPeremption int(5), -- nombre de jours avant la date de péremption
    primary key (refMateriel)
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


alter table `Utilisateur` add constraint fk_id_role foreign key (idRole) references `Role`(idRole);
alter table `Categorie` add constraint fk_code_domaine foreign key (codeD) references `Domaine`(codeD);
alter table `Materiel` add constraint fk_code_d_cat foreign key (codeD) references `Categorie`(codeD);
alter table `Materiel` add constraint fk_code_cat foreign key (codeC) references `Categorie`(codeC);
alter table `Commande` add constraint fk_id_util foreign key (idUti) references `Utilisateur`(idUti);
alter table `Commande` add constraint fk_ref_mat foreign key (refMateriel) references `Materiel`(refMateriel);
alter table `Commander` add constraint fk_id_uti foreign key (idUti) references `Utilisateur`(idUti);
alter table `Commander` add constraint fk_reference_mat foreign key (refMateriel) references `Materiel`(refMateriel);
