-- create database if not exists `GestLab` default character set utf8 collate utf8_general_ci;
-- use `GestLab`;

drop table if exists `Commander`;
drop table if exists `Commande`;
drop table if exists `Utilisateur`;
drop table if exists `Role`;
drop table if exists `AlerteSeuil`;
drop table if exists `AlerteQuantite`;
drop table if exists `MaterielInstance`;
drop table if exists `MaterielGenerique`;
drop table if exists `Categorie`;
drop table if exists `Domaine`;
drop table if exists `Statut`;


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

create table `MaterielGenerique`(
    refMateriel int(5),
    codeD int(5),
    codeC int(5),
    nomMateriel varchar(50),
    rangement varchar(50),
    commentaire varchar(50),
    qteMateriel int(5),    -- quantité globale du matériel
    qteMax int(5),    -- quantité maximale stockée dans l'établissement
    unite varchar(25),
    complements varchar(350),
    ficheFDS longblob,
    seuilQte int(5),    -- à environ 25% de la quantité du produit
    seuilPeremption int(3),    -- nombre de jours avant la date de péremption
    primary key (refMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `MaterielInstance`(
    idMateriel int(5),
    qteRestante int(5),
    datePeremption date, -- check (datePeremption > NOW()),
    refMateriel int(5),
    primary key (idMateriel, refMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Statut`(
    idStatut int(5),
    nomStatut varchar(50),
    primary key (idStatut)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Commande`(
    numeroCommande int(5),
    idUti int(5),
    refMateriel int(5),
    dateCommande date,
    dateReception date,
    idStatut int(5),
    primary key (numeroCommande, idUti, refMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `Commander`(
    numCommande int(5),
    idUti int(5),
    refMateriel int(5),
    qteCommandee int(5),
    primary key (numCommande, idUti, refMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `AlerteQuantite`(
    idAlerteQ int(5),
    refMateriel int(5),
    commentaire varchar(50),
    primary key (idAlerteQ)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `AlerteSeuil`(
    idAlerteS int(5),
    idMateriel int(5),
    commentaire varchar(50),
    primary key (idAlerteS)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

alter table `Utilisateur` add constraint fk_id_role foreign key (idRole) references `Role`(idRole);
alter table `Categorie` add constraint fk_code_domaine foreign key (codeD) references `Domaine`(codeD);
alter table `MaterielGenerique` add constraint fk_code_d_cat foreign key (codeD) references `Categorie`(codeD);
alter table `MaterielGenerique` add constraint fk_code_cat foreign key (codeC) references `Categorie`(codeC);
alter table `MaterielInstance` add constraint fk_reference_materiel foreign key (refMateriel) references `MaterielGenerique`(refMateriel);
alter table `Commande` add constraint fk_id_util foreign key (idUti) references `Utilisateur`(idUti);
alter table `Commande` add constraint fk_ref_mat foreign key (refMateriel) references `MaterielGenerique`(refMateriel);
alter table `Commande` add constraint fk_id_statut foreign key (idStatut) references `Statut`(idStatut);
alter table `Commander` add constraint fk_id_uti foreign key (idUti) references `Utilisateur`(idUti);
alter table `Commander` add constraint fk_reference_mat foreign key (refMateriel) references `MaterielGenerique`(refMateriel);
alter table `AlerteQuantite` add constraint fk_ref_mater foreign key (refMateriel) references `MaterielGenerique`(refMateriel);
alter table `AlerteSeuil` add constraint fk_ref_materiel foreign key (idMateriel) references `MaterielInstance`(idMateriel);