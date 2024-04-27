
-- Query di creazione del DataBase SwallowSpot

CREATE TABLE Area       -- zona di allerta per ogni rischio
(
    ID_area INT auto_increment,     -- ID univoco per ogni singola zona
    area_name VARCHAR(7),           -- nome della zona
    PRIMARY KEY (ID_area)
);

CREATE TABLE Risk       -- rischio specifico
(
    ID_risk INT auto_increment,     -- ID univoco per ogni rischio
    risk_name VARCHAR(35),          -- nome del tipo di rischio
    PRIMARY KEY (ID_risk)
);

CREATE TABLE Role       -- ruolo di ogni utente
(
    ID_role INT auto_increment,     -- ID univoco per ogni ruolo         
    role_name VARCHAR(35),          -- nome di ogni ruolo
    PRIMARY KEY (ID_role)
);

CREATE TABLE User       -- utente e i suoi dati
(
    ID_user INT auto_increment,         -- ID univoco per ogni utente
    username VARCHAR(35),               -- username usato dall'utente per registrarsi al sito
    password VARCHAR(48),               -- hash della password usata dall'utente per registrarsi al sito
    ID_area INT,                        -- area in cui vive
    ID_role INT,                        -- ruolo dell'utente nel sito
    PRIMARY KEY (ID_user),                           
    FOREIGN KEY (ID_area) REFERENCES Area(ID_area),
    FOREIGN KEY (ID_role) REFERENCES Role(ID_role)
);

CREATE TABLE Admin      -- admin del sito
(
    ID_telegram INT auto_increment,                 -- ID univoco per ogni 
    ID_user INT,                                    -- ID user dell'admin
    PRIMARY KEY (ID_telegram),
    FOREIGN KEY (ID_user) REFERENCES User(ID_user)
);

CREATE TABLE Report     -- bollettino
(
    ID_report INT auto_increment,       -- ID univoco per ogni bollettino
    starting_date DATETIME,             -- data di inizio validità
    ending_date DATETIME,               -- data di fine validità
    path VARCHAR(35),                   -- percorso del file nel server
    PRIMARY KEY (ID_report)
);

CREATE TABLE Snow_report        -- bollettino per gelate e valanghe
(
    ID_snow_report INT auto_increment,      -- ID univoco per ogni bollettino valanghe
    date DATETIME,                          -- data di inizio validità
    path VARCHAR(35),                       -- percorso del file nel server
    PRIMARY KEY (ID_snow_report)
);

CREATE TABLE Color      -- colori dei vari rischi
(
    ID_color INT auto_increment,        -- ID univoco per ogni colore
    color_name VARCHAR(35),             -- nome del colore di ogni tipo di rischio
    PRIMARY KEY (ID_color)
);

CREATE TABLE Criticalness       -- criticità
(
    ID_issue INT auto_increment,            -- ID univoco per ogni criticità
    ID_area INT,                            -- ID dell'area colpita dalla criticità
    ID_risk INT,                            -- ID del rischio associato
    ID_color INT,                           -- ID del colore
    PRIMARY KEY (ID_issue),
    FOREIGN KEY (ID_area) REFERENCES Area(ID_area),
    FOREIGN KEY (ID_risk) REFERENCES Risk(ID_risk),
    FOREIGN KEY (ID_color) REFERENCES Color(ID_color)
);

CREATE TABLE Topology       -- topologia
(
    city VARCHAR(35),               -- città univoca
    ID_area INT,                    -- ID dell'area a cui appartiene la città
    PRIMARY KEY(city),
    FOREIGN KEY (ID_area) REFERENCES Area(ID_area)
);

CREATE TABLE Report_criticalness        -- tabella ponte tra bollettini e criticità
(
    ID_report INT,                  -- ID del bollettino
    ID_issue INT,                   -- ID della criticità specifica
    PRIMARY KEY (ID_report, ID_issue),
    CONSTRAINT fk1 FOREIGN KEY (ID_report) REFERENCES Report(ID_report) ON DELETE CASCADE,
    CONSTRAINT fk2 FOREIGN KEY (ID_issue) REFERENCES Criticalness(ID_issue) ON DELETE CASCADE
);

CREATE TABLE Snow_report_criticalness        -- tabella ponte tra bollettini per valanghe e criticità
(
    ID_snow_report INT,                     -- ID del bollettino per neve
    ID_issue INT,                           -- ID della criticità specifica
    PRIMARY KEY (ID_snow_report, ID_issue),
    CONSTRAINT fk1 FOREIGN KEY (ID_snow_report) REFERENCES Snow_report(ID_snow_report) ON DELETE CASCADE,
    CONSTRAINT fk2 FOREIGN KEY (ID_issue) REFERENCES Criticalness(ID_issue) ON DELETE CASCADE
);







