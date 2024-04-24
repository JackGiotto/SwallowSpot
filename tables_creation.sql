
-- Query di creazione del DataBase SwallowSpot

create table Area       -- zona di allerta per ogni rischio
(
    ID_area int auto_increment,     -- ID univoco per ogni singola zona
    area_name varchar(7),           -- nome della zona
    primary key(ID_area)
);

create table Risk       -- rischio specifico
(
    ID_risk int auto_increment,     -- ID univoco per ogni rischio
    risk_name varchar(35),          -- nome del tipo di rischio
    primary key(ID_risk)
);

create table Role       -- ruolo di ogni utente
(
    ID_role int auto_increment,     -- ID univoco per ogni ruolo         
    role_name varchar(35),          -- nome di ogni ruolo
    primary key(ID_role)
);

create table User       -- utente e i suoi dati
(
    ID_user int auto_increment,         -- ID univoco per ogni utente
    -- email varchar(319),
    username varchar(35),               -- username usato dall'utente per registrarsi al sito
    password varchar(128),              -- hash della password usata dall'utente per registrarsi al sito
    ID_area int,                        -- area in cui vive
    ID_role int,                        -- ruolo dell'utente nel sito
    primary key(ID_user),                           
    foreign key (ID_area) references Area(ID_area),
    foreign key (ID_role) references Role(ID_role)
);

create table Admin      -- admin del sito
(
    ID_telegram int auto_increment,                 -- ID univoco per ogni 
    ID_user int,                                    -- ID user dell'admin
    primary key(ID_telegram),
    foreign key (ID_user) references User(ID_user)
);

create table Report     -- bollettino
(
    ID_report int auto_increment,       -- ID univoco per ogni bollettino
    starting_date datetime,             -- data di inizio validità / controllare se si può cambiare il formato YYYY-MM-DD HH:MI:SS
    ending_date datetime,               -- data di fine validità
    path varchar(35),                   -- percorso del file nel server
    primary key(ID_report)
);

create table Snow_report        -- bollettino per gelate e valanghe
(
    ID_snow_report int auto_increment,      -- ID univoco per ogni bollettino valanghe
    date datetime,                          -- data di inizio validità
    path varchar(35),                       -- percorso del file nel server
    primary key(ID_snow_report)
);

create table Color      -- colori dei vari rischi
(
    ID_color int auto_increment,        -- ID univoco per ogni colore
    color_name varchar(35),             -- nome del colore di ogni tipo di rischio
    primary key(ID_color)
);

create table Criticalness       -- criticità
(
    ID_issue int auto_increment,            -- ID univoco per ogni criticità
    ID_area int,                            -- ID dell'area colpita dalla criticità
    ID_risk int,                            -- ID del rischio associato
    ID_color int,                           -- ID del colore
    primary key(ID_issue),
    foreign key (ID_area) references Area(ID_area),
    foreign key (ID_risk) references Risk(ID_risk),
    foreign key (ID_color) references Color(ID_color)
);

create table Topology       -- topologia
(
    city varchar(35),               -- città univoca
    ID_area int,                    -- ID dell'area a cui appartiene la città
    primary key(city),
    foreign key (ID_area) references Area(ID_area)
);

create table Report_criticalness        -- tabella ponte tra bollettini e criticità
(
    ID_report int ,                             -- ID del bollettino
    ID_issue int,                               -- ID della criticità specifica
    primary key(ID_report, ID_issue),
    foreign key (ID_report) references Report(ID_report),
    foreign key (ID_issue) references Criticalness(ID_issue)
);

create table Snow_report_criticalness       -- tabella ponte tra bollettini per valanghe e criticità
(
    ID_snow_report int,                         -- ID del bollettino per neve
    ID_issue int,                               -- ID della criticità specifica
    primary key (ID_snow_report, ID_issue),
    foreign key (ID_snow_report) references Snow_report(ID_snow_report),
    foreign key (ID_issue) references Criticalness(ID_issue)
);






