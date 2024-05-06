-- visualizzare nomi delle città e relativa zona
SELECT Topology.city_name, Area.area_name
FROM Topology
JOIN Area ON Topology.ID_area = Area.ID_area 

-- selezionare utente e password per login
SELECT username, password
FROM User
WHERE username = 'name of the user' AND password = 'hash of the password';

-- controlla se un utente è admin
SELECT CASE
WHEN Admin.ID_user IS NOT NULL THEN 'True'
ELSE 'False'
END AS Is_Admin
FROM User
LEFT JOIN Admin ON User.ID_user = Admin.ID_user
WHERE User.username = 'username';

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
SELECT Report.starting_date, Report.ending_date, Color.color_name
FROM Report
JOIN Report_criticalness ON Report.ID_report = Report_criticalness.ID_report
JOIN Criticalness ON Report_criticalness.ID_issue = Criticalness.ID_issue
JOIN Area ON Criticalness.ID_area = Area.ID_area
JOIN Risk ON Criticalness.ID_risk = Risk.ID_risk
JOIN Color ON Criticalness.ID_color = Color.ID_color
WHERE Area.area_name = 'name of the area' AND Risk.risk_name = 'name of the risk'
ORDER BY Report.ID_report DESC 
LIMIT 1;

-- #68 Query to get last snow report for a specific area. The data that we should collect is: Starting date, three height of the area, three risk colors of the area
SELECT Snow_report.date, Snow_criticalness_altitude.value
FROM Snow_report
JOIN Snow_criticalness ON Snow_report.ID_snow_report = Snow_criticalness.ID_snow_report
JOIN Area ON Snow_criticalness.ID_area = Area.ID_area
JOIN Snow_criticalness_altitude ON Snow_criticalness.ID_snow_issue = Snow_criticalness_altitude.ID_snow_issue
WHERE Area.area_name = 'name of the area';

-- #69 Query to add last snow report to the database
SET @ID_area := (SELECT ID_area FROM Area WHERE area_name = 'name of the area');        -- Dichiarazione e assegnazione della variabile ID_area (assegna alla variabile l'ID specifico del nome dell'area)

SET @ID_snow_report := (SELECT LAST_INSERT_ID() FROM Snow_report); 

INSERT INTO Snow_criticalness(date, percentage, ID_area, ID_snow_report) VALUES 
('date of the criticalness', 'value of the percentage', @ID_area,  @ID_snow_report);

SET @ID_snow_issue := (SELECT LAST_INSERT_ID() FROM Snow_criticalness); 

SET @ID_altitude := (SELECT ID_altitude FROM Altitude WHERE height = 'value of the altitude(1000, 2000)'); 

INSERT INTO Snow_criticalness_altitude(ID_snow_issue, ID_altitude, value) VALUES
(@ID_snow_issue, @ID_altitude, 'value (5-10)');

-- i don't know if this variabile is overrided so it's better to create a new one
SET @ID_altitude := (SELECT ID_altitude FROM Altitude WHERE height = 'value of the altitude(1000, 2000)'); 

INSERT INTO Snow_criticalness_altitude(ID_snow_issue, ID_altitude, value) VALUES
(@ID_snow_issue, @ID_altitude, 'value (5-10)');

SET @ID_altitude := (SELECT ID_altitude FROM Altitude WHERE height = 'value of the altitude(1000, 2000)'); 

INSERT INTO Snow_criticalness_altitude(ID_snow_issue, ID_altitude, value) VALUES
(@ID_snow_issue, @ID_altitude, 'value (5-10)');