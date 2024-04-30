-- visualizzare nomi delle città e relativa zona
select city_name, area_name
from Topology
join Area on Topology.ID_area = Area.ID_area 

-- selezionare utente e password per login
select username, password
from User
where username = 'variabile_username' and password = 'variabile_password';

-- #20 Dovresti farmi una query che possa ottenere il livello di criticità di VENE B per ogni tipologia di pericolo, una per il primo bollettino e la stessa query per le nevicate 
-- dell'ultimo bollettino
select *
from Area
join Criticalness on Area.ID_area = Criticalness.ID_area
join Color on Criticalness.ID_color = Color.ID_color
join Risk on Criticalness.ID_risk = Risk.ID_risk
where area_name = 'variabile_area';

-- #60 You have to returning the list (by default dict json) by querys on our db so s02675 (stefani) can properly create the menu for the users during their sign-up
select city_name
from Topology;
