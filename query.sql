
-- Query di creazione del DataBase SwallowSpot

create table Area       -- zona di allerta per ogni rischio
(
    ID_area int auto_increment,     -- ID univoco per ogni singola zona
    area_name varchar(7),                        -- nome della zona
    primary key(ID_area)
);

create table Risk       -- rischio specifico
(
    ID_risk int auto_increment,     -- ID univoco per ogni rischio
    risk_name varchar(35),                       -- nome del tipo di rischio
    primary key(ID_risk)
);

create table Role       -- ruolo di ogni utente
(
    ID_role int auto_increment,     -- ID univoco per ogni ruolo         
    role_name varchar(35),                      -- nome di ogni ruolo
    primary key(ID_role)
);

create table User       -- utente e i suoi dati
(
    ID_user int auto_increment,         -- ID univoco per ogni utente
    username varchar(35),                           -- username usato dall'utente per registrarsi al sito
    password varchar(128),                          -- hash della password usata dall'utente per registrarsi al sito
    ID_area int,                                    -- area in cui vive
    ID_role int,                                    -- ruolo dell'utente nel sito
    primary key(ID_user),    
    foreign key (ID_area) references Area(ID_area),
    foreign key (ID_role) references Role(ID_role)
);

create table Admin
(
    ID_telegram int auto_increment,
    ID_user int,
    primary key(ID_telegram),
    foreign key (ID_user) references User(ID_user)
);

create table Report
(
    ID_report int auto_increment,
    starting_date datetime,                     -- controllare se si può cambiare il formato YYYY-MM-DD HH:MI:SS
    ending_date datetime,       
    path varchar(35),
    primary key(ID_report)
);

create table Snow_report
(
    ID_snow_report int auto_increment,
    date datetime,
    path varchar(35),
    primary key(ID_snow_report)
);

create table Color
(
    ID_color int auto_increment,
    color_name varchar(35),
    primary key(ID_color)
);

create table Criticalness
(
    ID_issue int auto_increment,
    ID_area int,
    ID_risk int,
    ID_color int,
    primary key(ID_issue),
    foreign key (ID_area) references Area(ID_area),
    foreign key (ID_risk) references Risk(ID_risk),
    foreign key (ID_color) references Color(ID_color)
);

create table Topology
(
    city varchar(35),
    ID_area int,
    primary key(city)
    foreign key (ID_area) references Area(ID_area)
);

create table Report_criticalness
(
    ID_report int ,
    ID_issue int,
    primary key(ID_report, ID_issue)
    foreign key (ID_report) references Report(ID_report),
    foreign key (ID_issue) references Criticalness(ID_issue)
);

create table Snow_report_criticalness
(
    ID_snow_report int,
    ID_issue int,
    primary key (ID_snow_report, ID_issue)
    foreign key (ID_snow_report) references Snow_report(ID_snow_report),
    foreign key (ID_issue) references Criticalness(ID_issue)
);






