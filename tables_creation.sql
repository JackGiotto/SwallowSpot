
-- Query di creazione del DataBase SwallowSpot

CREATE TABLE Area       -- zona di allerta per ogni rischio
(
    ID_area INT AUTO_INCREMENT,                 -- ID univoco per ogni singola zona
    area_name VARCHAR(35) NOT NULL UNIQUE,       -- nome della zona
    CONSTRAINT pk_area PRIMARY KEY (ID_area)    -- vincolo di chiave primaria di Area
);

CREATE TABLE Risk       -- rischio specifico
(
    ID_risk INT AUTO_INCREMENT,                 -- ID univoco per ogni rischio
    risk_name VARCHAR(35) NOT NULL UNIQUE,      -- nome del tipo di rischio
    CONSTRAINT pk_risk PRIMARY KEY (ID_risk)    -- vincolo di chiave primaria di Risk
);

CREATE TABLE Role       -- ruolo di ogni utente
(
    ID_role INT AUTO_INCREMENT,                     -- ID univoco per ogni ruolo         
    role_name VARCHAR(35) NOT NULL UNIQUE,          -- nome di ogni ruolo
    CONSTRAINT pk_role PRIMARY KEY (ID_role)        -- vincolo di chiave primaria di Role
);

CREATE TABLE Color      -- colori dei vari rischi
(
    ID_color INT AUTO_INCREMENT,                -- ID univoco per ogni colore
    color_name VARCHAR(35) NOT NULL UNIQUE,     -- nome del colore di ogni tipo di rischio
    CONSTRAINT pk_color PRIMARY KEY (ID_color)      -- vincolo di chiave primaria di Color
);

CREATE TABLE User       -- utente e i suoi dati
(
    ID_user INT AUTO_INCREMENT,                         -- ID univoco per ogni utente
    username VARCHAR(35) NOT NULL UNIQUE,               -- username usato dall'utente per registrarsi al sito
    password VARCHAR(64) NOT NULL,                      -- hash della password usata dall'utente per registrarsi al sito
    ID_area INT NOT NULL,                               -- zona in cui vive
    ID_role INT NOT NULL,                               -- ruolo dell'utente nel sito
    CONSTRAINT pk_user PRIMARY KEY (ID_user),           -- vincolo di chiave primaria di User                                
    CONSTRAINT fk_user_area FOREIGN KEY (ID_area) REFERENCES Area(ID_area) ON UPDATE CASCADE ON DELETE CASCADE,     -- vincolo di chiave esterna relativa alla zona
    CONSTRAINT fk_user_role FOREIGN KEY (ID_role) REFERENCES Role(ID_role) ON UPDATE CASCADE ON DELETE CASCADE      -- vincolo di chiave esterna relativa al ruolo
);

CREATE TABLE Admin      -- amministratori del sito
(
    ID_telegram VARCHAR(15),                            -- ID assegnato da telegram per ogni amministratore
    ID_user INT NOT NULL,                               -- ID user dell'admin
    CONSTRAINT pk_admin PRIMARY KEY (ID_telegram),      -- vincolo di chiave primaria di Admin
    CONSTRAINT fk_admin_user FOREIGN KEY (ID_user) REFERENCES User(ID_user) ON UPDATE CASCADE ON DELETE CASCADE     -- vincolo di chiave esterna relativo all'utente
);

CREATE TABLE Report     -- bollettino
(
    ID_report INT AUTO_INCREMENT,           -- ID univoco per ogni bollettino
    starting_date DATETIME NOT NULL,        -- data di inizio validità
    ending_date DATETIME NOT NULL,          -- data di fine validità
    path VARCHAR(35) NOT NULL UNIQUE,       -- percorso del file nel server
    CONSTRAINT pk_report PRIMARY KEY (ID_report)        -- vincolo di chiave primaria di Report
);

/*
CREATE TABLE Snow_report        -- bollettino per gelate e valanghe
(
    ID_snow_report INT AUTO_INCREMENT,      -- ID univoco per ogni bollettino valanghe
    date DATETIME NOT NULL,                 -- data di inizio validità
    path VARCHAR(35) NOT NULL UNIQUE,       -- percorso del file nel server
    CONSTRAINT pk_snow_report PRIMARY KEY (ID_snow_report)      -- vincolo di chiave primaria di Snow_report
);
*/

CREATE TABLE Criticalness       -- criticità presenti all'interno dei bollettini
(
    ID_issue INT AUTO_INCREMENT,        -- ID univoco per ogni criticità
    ID_area INT NOT NULL,               -- ID dell'area colpita dalla criticità
    ID_risk INT NOT NULL,               -- ID del rischio associato
    ID_color INT NOT NULL,              -- ID del colore
    CONSTRAINT pk_criticalness PRIMARY KEY (ID_issue),      -- vincolo di chiave primaria di Criticalness
    CONSTRAINT fk_criticalness_area FOREIGN KEY (ID_area) REFERENCES Area(ID_area) ON UPDATE CASCADE ON DELETE CASCADE,     -- vincolo di chiave esterna relativa alla zona
    CONSTRAINT fk_criticalness_risk FOREIGN KEY (ID_risk) REFERENCES Risk(ID_risk) ON UPDATE CASCADE ON DELETE CASCADE,     -- vincolo di chiave esterna relativa al rischio
    CONSTRAINT fk_criticalness_color FOREIGN KEY (ID_color) REFERENCES Color(ID_color) ON UPDATE CASCADE ON DELETE CASCADE  -- vincolo di chiave esterna relativa al colore
);

CREATE TABLE Topology       -- topologia delle città e delle zone di rischio
(
    ID_city INT AUTO_INCREMENT,                 -- ID univoco
    city_name VARCHAR(35) NOT NULL UNIQUE,      -- nome della città 
    ID_area INT NOT NULL,                       -- ID dell'area a cui appartiene la città
    CONSTRAINT pk_topology PRIMARY KEY (ID_city),       -- vincolo di chiave primaria di Topology
    CONSTRAINT fk_topology_area FOREIGN KEY (ID_area) REFERENCES Area(ID_area) ON UPDATE CASCADE ON DELETE CASCADE      -- vincolo di chiave esterna relativa alla zona
);


CREATE TABLE Report_criticalness        -- tabella ponte tra bollettini e criticità
(
    ID_report INT NOT NULL,     -- ID del bollettino
    ID_issue INT NOT NULL,      -- ID della criticità specifica
    CONSTRAINT pk_report_criticalness PRIMARY KEY (ID_report, ID_issue),        -- vincolo di chiave primaria di Report_criticalness
    CONSTRAINT fk_report FOREIGN KEY (ID_report) REFERENCES Report(ID_report) ON UPDATE CASCADE ON DELETE CASCADE,              -- vincolo di chiave esterna relativa al bollettino
    CONSTRAINT fk_criticalness FOREIGN KEY (ID_issue) REFERENCES Criticalness(ID_issue) ON UPDATE CASCADE ON DELETE CASCADE     -- vincolo di chiave esterna relativa alla criticità
);

/*
CREATE TABLE Snow_report_criticalness        -- tabella ponte tra bollettini per valanghe e criticità
(
    ID_snow_report INT NOT NULL,        -- ID del bollettino per neve
    ID_snow_issue INT NOT NULL,              -- ID della criticità specifica
    CONSTRAINT pk_snow_report_criticalness PRIMARY KEY (ID_snow_report, ID_snow_issue),      -- vincolo di chiave primaria composta di Snow_report_criticalness
    CONSTRAINT fk_snow_report FOREIGN KEY (ID_snow_report) REFERENCES Snow_report(ID_snow_report) ON UPDATE CASCADE ON DELETE CASCADE,      -- vincolo di chiave esterna relativa al bollettino per neve
    CONSTRAINT fk_snow_criticalness FOREIGN KEY (ID_snow_issue) REFERENCES Criticalness(ID_issue) ON UPDATE CASCADE ON DELETE CASCADE                 -- vincolo di chiave esterna relativa alla criticità
);
*/

CREATE TABLE Altitude
(
    ID_altitude INT AUTO_INCREMENT,
    height VARCHAR(15) NOT NULL UNIQUE,
    CONSTRAINT pk_altitude PRIMARY KEY (ID_altitude)
);

CREATE TABLE Snow_criticalness
(
    ID_snow_issue INT AUTO_INCREMENT,
    date DATETIME NOT NULL,
    percentage INT NOT NULL,
    ID_area INT NOT NULL,
    CONSTRAINT pk_snow_issue PRIMARY KEY (ID_snow_issue),
    CONSTRAINT fk_snow_criticalness_area FOREIGN KEY (ID_area) REFERENCES Area(ID_area) ON UPDATE CASCADE ON DELETE CASCADE      -- vincolo di chiave esterna relativa alla zona
);

CREATE TABLE Snow_criticalness_altitude
(
    ID_snow_issue INT NOT NULL,      -- ID della criticità per neve
    ID_altitude INT NOT NULL,      -- ID della criticità per neve
    value VARCHAR(15) NOT NULL,
    CONSTRAINT pk__criticalness PRIMARY KEY (ID_snow_issue, ID_altitude),        -- vincolo di chiave primaria di 
    CONSTRAINT fk_snow_issue FOREIGN KEY (ID_snow_issue) REFERENCES Snow_criticalness(ID_snow_issue) ON UPDATE CASCADE ON DELETE CASCADE,              -- vincolo di chiave esterna 
    CONSTRAINT fk_altitude FOREIGN KEY (ID_altitude) REFERENCES Altitude(ID_altitude) ON UPDATE CASCADE ON DELETE CASCADE     -- vincolo di chiave esterna 
);

/*
-- debug

DROP TABLE Snow_report_criticalness;
DROP TABLE Report_criticalness;
DROP TABLE Topology;
DROP TABLE Criticalness;
DROP TABLE Color;
DROP TABLE Snow_report;
DROP TABLE Report;
DROP TABLE Admin;
DROP TABLE User;
DROP TABLE Role;
DROP TABLE Risk;
DROP TABLE Area;

*/






