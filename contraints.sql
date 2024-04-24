
alter table Area        -- tabella delle zone
modify column area_name not null,   -- nome della zona diverso da Null
add unique (area_name);             -- nome della zona univoco

alter table Risk
modify column risk_name not null,
add unique (risk_name);

alter table Role
modify column role_name not null,
add unique (role_nome);

alter table User
add unique (username);
