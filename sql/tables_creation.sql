-- Queries for SwallowSpot's Database creation

CREATE TABLE Area       -- list of the areas
(
    ID_area INT AUTO_INCREMENT,                     -- unique ID for every area
    area_name VARCHAR(35) NOT NULL UNIQUE,          -- area's name
    CONSTRAINT pk_area PRIMARY KEY (ID_area)        -- PK constraint
);

CREATE TABLE Risk       -- list of the risks
(
    ID_risk INT AUTO_INCREMENT,                     -- unique ID for every area
    risk_name VARCHAR(35) NOT NULL UNIQUE,          -- risk's name
    CONSTRAINT pk_risk PRIMARY KEY (ID_risk)        -- PK constraint
);

CREATE TABLE Role       -- list of the roles
(
    ID_role INT AUTO_INCREMENT,                     -- unique ID for every role        
    role_name VARCHAR(35) NOT NULL UNIQUE,          -- role's name
    CONSTRAINT pk_role PRIMARY KEY (ID_role)        -- PK constraint
);

CREATE TABLE Color      -- list of the colors
(
    ID_color INT AUTO_INCREMENT,                    -- unique ID for every color
    color_name VARCHAR(35) NOT NULL UNIQUE,         -- color's name
    CONSTRAINT pk_color PRIMARY KEY (ID_color)      -- PK constraint
);

CREATE TABLE Altitude       -- list of the altitudes
(
    ID_altitude INT AUTO_INCREMENT,                         -- unique ID for every altitude
    height VARCHAR(10) NOT NULL UNIQUE,                     -- value of the height                 
    CONSTRAINT pk_altitude PRIMARY KEY (ID_altitude)        -- PK constraint
);

CREATE TABLE Report     -- list of the bulletins
(
    ID_report INT AUTO_INCREMENT,                       -- unique ID for every bulletin
    starting_date DATETIME NOT NULL UNIQUE,             -- data di inizio validità
    ending_date DATETIME NOT NULL,                      -- data di fine validità
    path VARCHAR(70) NOT NULL UNIQUE,                   -- percorso del file nel server
    CONSTRAINT pk_report PRIMARY KEY (ID_report)        -- PK constraint
);


CREATE TABLE Criticalness       -- list of the criticalnesses into reports
(
    ID_issue INT AUTO_INCREMENT,                            -- unique ID for every criticalness
    ID_area INT NOT NULL,                                   -- area's ID
    ID_risk INT NOT NULL,                                   -- risk's ID
    ID_color INT NOT NULL,                                  -- color's ID
    ID_report INT NOT NULL,                                 -- report's ID
    CONSTRAINT pk_criticalness PRIMARY KEY (ID_issue),      -- PK constraint
    CONSTRAINT fk_criticalness_area FOREIGN KEY (ID_area) REFERENCES Area(ID_area) ON UPDATE CASCADE ON DELETE CASCADE,             -- FK constraint from Area identifier
    CONSTRAINT fk_criticalness_risk FOREIGN KEY (ID_risk) REFERENCES Risk(ID_risk) ON UPDATE CASCADE ON DELETE CASCADE,             -- FK constraint from Role identifier
    CONSTRAINT fk_criticalness_color FOREIGN KEY (ID_color) REFERENCES Color(ID_color) ON UPDATE CASCADE ON DELETE CASCADE,         -- FK constraint from Color identifier
    CONSTRAINT fk_criticalness_report FOREIGN KEY (ID_report) REFERENCES Report(ID_report) ON UPDATE CASCADE ON DELETE CASCADE      -- FK constraint from Report identifier
);

CREATE TABLE Snow_report        -- list of the bulletins for snow event   
(
    ID_snow_report INT AUTO_INCREMENT,      -- unique ID for every snow bulletin
    date DATETIME NOT NULL UNIQUE,          -- data from which the report is valid
    path VARCHAR(70) NOT NULL UNIQUE,       -- path of the file into the server
    CONSTRAINT pk_snow_report PRIMARY KEY (ID_snow_report)      -- PK constraint
);

CREATE TABLE Snow_criticalness      -- list of the criticalnesses into snow reports
(
    ID_snow_issue INT AUTO_INCREMENT,
    date DATETIME NOT NULL,
    percentage INT NOT NULL,
    ID_area INT NOT NULL,
    ID_snow_report INT NOT NULL,
    CONSTRAINT pk_snow_issue PRIMARY KEY (ID_snow_issue),       -- PK constraint
    CONSTRAINT fk_snow_criticalness_report FOREIGN KEY (ID_snow_report) REFERENCES Snow_report(ID_snow_report) ON UPDATE CASCADE ON DELETE CASCADE,     -- FK constraint from Report identifier
    CONSTRAINT fk_snow_criticalness_area FOREIGN KEY (ID_area) REFERENCES Area(ID_area) ON UPDATE CASCADE ON DELETE CASCADE                             -- FK constraint from Area identifier
);

CREATE TABLE Topology       -- list of the cities associated with each area
(
    ID_city INT AUTO_INCREMENT,                 -- ID univoco
    city_name VARCHAR(35) NOT NULL UNIQUE,      -- nome della città 
    ID_area INT NOT NULL,                       -- ID dell'area a cui appartiene la città
    CONSTRAINT pk_topology PRIMARY KEY (ID_city),       -- PK constraint
    CONSTRAINT fk_topology_area FOREIGN KEY (ID_area) REFERENCES Area(ID_area) ON UPDATE CASCADE ON DELETE CASCADE      -- FK constraint from Area identifier
);

CREATE TABLE User       -- list of the Users' accounts and their data
(
    ID_user INT AUTO_INCREMENT,                         -- ID univoco per ogni utente
    username VARCHAR(35) NOT NULL UNIQUE,               -- username usato dall'utente per registrarsi al sito
    password VARCHAR(64) NOT NULL,                      -- hash della password usata dall'utente per registrarsi al sito
    ID_area INT NOT NULL,                               -- zona in cui vive
    ID_role INT NOT NULL,                               -- ruolo dell'utente nel sito
    CONSTRAINT pk_user PRIMARY KEY (ID_user),       -- PK constraint                             
    CONSTRAINT fk_user_area FOREIGN KEY (ID_area) REFERENCES Area(ID_area) ON UPDATE CASCADE ON DELETE CASCADE,     -- FK constraint from Area identifier
    CONSTRAINT fk_user_role FOREIGN KEY (ID_role) REFERENCES Role(ID_role) ON UPDATE CASCADE ON DELETE CASCADE      -- FK constraint from Role identifier
);

CREATE TABLE Admin      -- list of the administration account
(
    ID_telegram VARCHAR(15),                            -- ID assegnato da telegram per ogni amministratore
    groupID VARCHAR(15) NOT NULL UNIQUE,
    ID_user INT NOT NULL,                               -- ID user dell'admin
    CONSTRAINT pk_admin PRIMARY KEY (ID_telegram),      -- PK constraint
    CONSTRAINT fk_admin_user FOREIGN KEY (ID_user) REFERENCES User(ID_user) ON UPDATE CASCADE ON DELETE CASCADE     -- FK constraint from User identifier
);

CREATE TABLE Snow_criticalness_altitude     -- list every snow criticalness connected with each altitude
(
    ID_snow_issue INT NOT NULL,                                                 -- ID della criticità per neve
    ID_altitude INT NOT NULL,                                                   -- ID della criticità per neve
    value VARCHAR(15) NOT NULL,                                                 -- value of the snow level
    CONSTRAINT pk__criticalness PRIMARY KEY (ID_snow_issue, ID_altitude),       -- PK constraint
    CONSTRAINT fk_snow_issue FOREIGN KEY (ID_snow_issue) REFERENCES Snow_criticalness(ID_snow_issue) ON UPDATE CASCADE ON DELETE CASCADE,       -- FK constraint from Snow Criticalness identifier
    CONSTRAINT fk_altitude FOREIGN KEY (ID_altitude) REFERENCES Altitude(ID_altitude) ON UPDATE CASCADE ON DELETE CASCADE                       -- FK constraint from Altitude identifier
);

/*
-- debug
DROP TABLE Snow_criticalness_altitude;
DROP TABLE Admin;
DROP TABLE User;
DROP TABLE Topology;
DROP TABLE Snow_criticalness;
DROP TABLE Snow_report;
DROP TABLE Criticalness;
DROP TABLE Report;
DROP TABLE Altitude;
DROP TABLE Color;
DROP TABLE Role;
DROP TABLE Risk;
DROP TABLE Area;
*/





