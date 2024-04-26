
alter table Area        -- modifica tabella delle zone
modify column area_name varchar(7) not null,    -- nome della zona diverso da Null
add unique (area_name);                         -- nome della zona univoco

alter table Risk        -- modifica tabella dei rischi
modify column risk_name varchar(35) not null,
add unique (risk_name);

alter table Role        -- modifica tabella dei ruoli
modify column role_name varchar(35) not null,
add unique (role_nome);

alter table User        -- modifica tabella degli utenti
modify column username not null,
modify column password not null,
add unique (username);

alter table Admin       -- modifica tabella degli amministratori

alter table Report      -- modifica tabella dei bollettini

alter table Snow_report         -- modifica tabella dei bollettini per neve

alter table Color       -- modifica tabella dei colori

alter table Criticalness        -- modifica tabella delle criticità

alter table Topology        -- modifica tabella della topologia