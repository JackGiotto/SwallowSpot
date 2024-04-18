
create table topology       -- assegnazione delle città alle rispettive zone di rischio
(
    city varchar(35) primary key not null,          -- nome della città
    area varchar(5) not null                        -- sigla della zona
)

