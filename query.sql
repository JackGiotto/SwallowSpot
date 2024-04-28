-- visualizzare nomi delle città e relativa zona
select city_name, area_name
from Topology
join Area on Topology.ID_area = Area.ID_area 