-- visualizzare nomi delle città e relativa zona
SELECT Topology.city_name, Area.area_name
FROM Topology
JOIN Area ON Topology.ID_area = Area.ID_area 

-- selezionare utente e password per login
SELECT username, password
FROM User
WHERE username = 'name of the user' AND password = 'hash of the password';

-- #20 Dovresti farmi una query che possa ottenere il livello di criticità di VENE B per ogni tipologia di pericolo, una per il primo bollettino e la stessa query per le nevicate 
-- dell'ultimo bollettino
SELECT *
FROM Area
JOIN Criticalness ON Area.ID_area = Criticalness.ID_area
JOIN Color ON Criticalness.ID_color = Color.ID_color
JOIN Risk ON Criticalness.ID_risk = Risk.ID_risk
WHERE Area.area_name = 'name of the area';

-- #60 You have to returning the list (by default dict JSON) by querys on our db so s02675 (stefani) can properly create the menu for the users during their sign-up
SELECT city_name
FROM Topology;

-- #62 Make a query to get the Area of a specific user
SELECT User.username, Area.area_name
FROM User
JOIN Area ON User.ID_area = Area.ID_area
WHERE User.username = 'name of the user';

-- #58 Create queries to add the risks collected by the bulletin to the database. Hydro and snow risks are more important than avalanche risks, so it's better to focus on these first.

SET @ID_area := (SELECT ID_area FROM Area WHERE area_name = 'name of the area');        -- Dichiarazione e assegnazione della variabile ID_area (assegna alla variabile l'ID specifico del nome dell'area)

SET @ID_risk := (SELECT ID_risk FROM Risk WHERE risk_name = 'name of the risk');        -- Dichiarazione e assegnazione della variabile ID_risk

SET @ID_color := (SELECT ID_color FROM Color WHERE color_name = 'name of the color');        -- Dichiarazione e assegnazione della variabile ID_color

INSERT INTO Criticalness(ID_area, ID_risk, ID_color) VALUES 
(@ID_area, @ID_risk, @ID_color);

-- #63 Create a query to get the last bulletin data of a specific Area. The data we need is: 3 risks level, date
SELECT Report.starting_date, Report.ending_date
FROM Report
JOIN Report_criticalness ON Report.ID_report = Report_criticalness.ID_report
JOIN Criticalness ON Report_criticalness.ID_issue = Criticalness.ID_issue
JOIN Area ON Criticalness.ID_area = Area.ID_area
JOIN Risk ON Criticalness.ID_risk = Risk.ID_risk
WHERE Area.area_name = 'name of the area' and Risk.risk_name = 'name of the risk'
ORDER BY Report.ID_report DESC 
LIMIT 1;