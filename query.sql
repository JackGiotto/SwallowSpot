
create table topology       -- assegnazione delle città alle rispettive zone di rischio
(
    city varchar(35) primary key not null,          -- nome della città
    ID_area int not null,
    constraint FK1_topology foreign key (ID_area) references area(ID_area) on delete cascade 
)

create table area
(
    ID_area int primary key not null auto_increment,
    area_name varchar(5)
)

