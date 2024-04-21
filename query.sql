
-- Query di creazione del DataBase SwallowSpot

create table Area       -- zona di allerta per ogni rischio
(
    ID_area int auto_increment primary key,     -- ID univoco per ogni singola zona
    area_name varchar(7)                        -- nome della zona
);

create table Risk       -- rischio specifico
(
    ID_risk int auto_increment primary key,     -- ID univoco per ogni rischio
    risk_name varchar(35)                       -- nome del tipo di rischio
);

create table Role       -- ruolo di ogni utente
(
    ID_role int auto_increment primary key,     -- ID univoco per ogni ruolo         
    role_name varchar(35)                       -- nome di ogni ruolo
);

create table User       -- utente e i suoi dati
(
    ID_user int auto_increment primary key,         -- ID univoco per ogni utente
    username varchar(35),                           -- username usato dall'utente per registrarsi al sito
    password varchar(128),                          -- hash della password usata dall'utente per registrarsi al sito
    ID_area int,                                    -- area in cui vive
    ID_role int,                                    -- ruolo dell'utente nel sito
    foreign key (ID_area) references Area(ID_area),
    foreign key (ID_role) references Role(ID_role)
);

