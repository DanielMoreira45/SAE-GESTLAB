-- create database if not exists `GestLab` default character set utf8 collate utf8_general_ci;
-- use `GestLab`;

drop table if exists `COMMANDER`;
drop table if exists `COMMANDE`;
drop table if exists `UTILISATEUR`;
drop table if exists `ROLE`;
drop table if exists `ALERTESEUIL`;
drop table if exists `ALERTEQUANTITE`;
drop table if exists `MATERIELINSTANCE`;
drop table if exists `MATERIELGENERIQUE`;
drop table if exists `CATEGORIE`;
drop table if exists `DOMAINE`;
drop table if exists `STATUT`;


create table `ROLE`(
    idRole int(5),
    intitule varchar(50),
    primary key (idRole)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `UTILISATEUR`(
    idUti int(5),
    idRole int(5),
    nomUti varchar(50),
    prenomUti varchar(50),
    emailUti varchar(50),
    mdp varchar(50),
    modifications boolean,
    primary key (idUti)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `DOMAINE`(
    codeD int(5),
    nomD varchar(50),
    primary key (codeD)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `CATEGORIE`(
    codeC int(5),
    codeD int(5),
    nomC varchar(50),
    primary key (codeC, codeD)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `MATERIELGENERIQUE`(
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
    ficheFDS varchar(50),
    seuilQte int(5),    -- à environ 25% de la quantité du produit
    seuilPeremption int(3),    -- nombre de jours avant la date de péremption
    imageMateriel longblob,
    primary key (refMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `MATERIELINSTANCE`(
    idMateriel int(5),
    qteRestante int(5),
    datePeremption date, -- check (datePeremption > NOW()),
    refMateriel int(5),
    primary key (idMateriel, refMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `STATUT`(
    idStatut int(5),
    nomStatut varchar(50),
    primary key (idStatut)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `COMMANDE`(
    numeroCommande int(5),
    idUti int(5),
    refMateriel int(5),
    dateCommande date,
    dateReception date,
    qteCommandee int(5),
    idStatut int(5),
    primary key (numeroCommande, idUti, refMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `COMMANDER`(
    numCommande int(5),
    idUti int(5),
    refMateriel int(5),
    qteCommandee int(5),
    primary key (numCommande, idUti, refMateriel)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `ALERTEQUANTITE`(
    idAlerteQ int(5),
    refMateriel int(5),
    commentaire varchar(50),
    primary key (idAlerteQ)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

create table `ALERTESEUIL`(
    idAlerteS int(5),
    idMateriel int(5),
    commentaire varchar(50),
    primary key (idAlerteS)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8;

alter table `UTILISATEUR` add constraint fk_id_role foreign key (idRole) references `ROLE`(idRole);
alter table `CATEGORIE` add constraint fk_code_domaine foreign key (codeD) references `DOMAINE`(codeD);
alter table `MATERIELGENERIQUE` add constraint fk_code_d_cat foreign key (codeD) references `CATEGORIE`(codeD);
alter table `MATERIELGENERIQUE` add constraint fk_code_cat foreign key (codeC) references `CATEGORIE`(codeC);
alter table `MATERIELINSTANCE` add constraint fk_reference_materiel foreign key (refMateriel) references `MATERIELGENERIQUE`(refMateriel);
alter table `COMMANDE` add constraint fk_id_util foreign key (idUti) references `UTILISATEUR`(idUti);
alter table `COMMANDE` add constraint fk_ref_mat foreign key (refMateriel) references `MATERIELGENERIQUE`(refMateriel);
alter table `COMMANDE` add constraint fk_id_statut foreign key (idStatut) references `STATUT`(idStatut);
alter table `COMMANDER` add constraint fk_id_uti foreign key (idUti) references `UTILISATEUR`(idUti);
alter table `COMMANDER` add constraint fk_reference_mat foreign key (refMateriel) references `MATERIELGENERIQUE`(refMateriel);
alter table `ALERTEQUANTITE` add constraint fk_ref_mater foreign key (refMateriel) references `MATERIELGENERIQUE`(refMateriel);
alter table `ALERTESEUIL` add constraint fk_ref_materiel foreign key (idMateriel) references `MATERIELINSTANCE`(idMateriel);