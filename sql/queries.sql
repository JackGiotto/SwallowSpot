-- Certificated query to select and insert data from the DB

-- To get every city associated with the area
SELECT Topology.city_name, Area.area_name
FROM Topology
JOIN Area ON Topology.ID_area = Area.ID_area 

-- For login
SELECT username, password
FROM User
WHERE username = 'name of the user' AND password = 'hash of the password';

-- Control if an user is an admin
SELECT CASE
WHEN Admin.ID_user IS NOT NULL THEN 'True'
ELSE 'False'
END AS Is_Admin
FROM User
LEFT JOIN Admin ON User.ID_user = Admin.ID_user
WHERE User.username = 'username';

-- For issue #20 
SELECT *
FROM Area
JOIN Criticalness ON Area.ID_area = Criticalness.ID_area
JOIN Color ON Criticalness.ID_color = Color.ID_color
JOIN Risk ON Criticalness.ID_risk = Risk.ID_risk
WHERE Area.area_name = 'name of the area';

-- For issue #60
SELECT city_name
FROM Topology;

-- For issue #62
SELECT User.username, Area.area_name
FROM User
JOIN Area ON User.ID_area = Area.ID_area
WHERE User.username = 'name of the user';

-- For issue #58
SET @ID_area := (SELECT ID_area FROM Area WHERE area_name = 'name of the area');        -- insert the value of the query into the @variable      
SET @ID_risk := (SELECT ID_risk FROM Risk WHERE risk_name = 'name of the risk');        
SET @ID_color := (SELECT ID_color FROM Color WHERE color_name = 'name of the color');   

INSERT INTO Criticalness(ID_area, ID_risk, ID_color) VALUES 
(@ID_area, @ID_risk, @ID_color);

-- For issue #63
SELECT Report.starting_date, Report.ending_date, Color.color_name
FROM Report
JOIN Criticalness ON Report.ID_report = Criticalness.ID_report
JOIN Area ON Criticalness.ID_area = Area.ID_area
JOIN Risk ON Criticalness.ID_risk = Risk.ID_risk
JOIN Color ON Criticalness.ID_color = Color.ID_color
WHERE Area.area_name = 'VENE-A' AND Risk.risk_name = 'idraulico'
ORDER BY starting_date DESC
LIMIT 1;

-- For issue #68
SELECT Snow_report.date, Snow_criticalness_altitude.value
FROM Snow_report
JOIN Snow_criticalness ON Snow_report.ID_snow_report = Snow_criticalness.ID_snow_report
JOIN Area ON Snow_criticalness.ID_area = Area.ID_area
JOIN Snow_criticalness_altitude ON Snow_criticalness.ID_snow_issue = Snow_criticalness_altitude.ID_snow_issue
WHERE Area.area_name = 'name of the area';

-- For issue #69
SET @ID_area := (SELECT ID_area FROM Area WHERE area_name = 'name of the area');       
SET @ID_snow_report := (SELECT LAST_INSERT_ID() FROM Snow_report); 

INSERT INTO Snow_criticalness(date, percentage, ID_area, ID_snow_report) VALUES 
('date of the criticalness', 'value of the percentage', @ID_area,  @ID_snow_report);

SET @ID_snow_issue := (SELECT LAST_INSERT_ID() FROM Snow_criticalness); 
SET @ID_altitude := (SELECT ID_altitude FROM Altitude WHERE height = 'value of the altitude(1000, 2000)'); 

INSERT INTO Snow_criticalness_altitude(ID_snow_issue, ID_altitude, value) VALUES
(@ID_snow_issue, @ID_altitude, 'value (5-10)');

SET @ID_altitude := (SELECT ID_altitude FROM Altitude WHERE height = 'value of the altitude(1000, 2000)'); 

INSERT INTO Snow_criticalness_altitude(ID_snow_issue, ID_altitude, value) VALUES
(@ID_snow_issue, @ID_altitude, 'value (5-10)');

SET @ID_altitude := (SELECT ID_altitude FROM Altitude WHERE height = 'value of the altitude(1000, 2000)'); 

INSERT INTO Snow_criticalness_altitude(ID_snow_issue, ID_altitude, value) VALUES
(@ID_snow_issue, @ID_altitude, 'value (5-10)');

-- Insertion of pdf file into database BLOB
INSERT INTO pdf_files (starting_date, ending_date, pdf_data)
VALUES ("starting-data format datetime", "ending date format datetime", "pdf in bites")

-- For issue #4 V2
INSERT INTO Feedback (object, description, date, validate, ID_role) VALUES
('title of the feedback (object)', 'description of the feedback', NOW(), false, 'user ID');

-- For issue #13 V2
INSERT INTO Snake (high_score, ID_user) VALUES
('high score of the user', 'user ID');
