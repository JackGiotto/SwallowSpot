-- default data into the DB

INSERT INTO Area (area_name) VALUES     -- risk areas 
    ('Vene-A'), 
    ('Vene-H'),
    ('Vene-B'),
    ('Vene-C'),
    ('Vene-D'),
    ('Vene-E'),
    ('Vene-F'),
    ('Vene-G'),
    ('Mont-1A'),
    ('Mont-1B'),
    ('Mont-1C'),
    ('Mont-1D'),
    ('Mont-2A'),
    ('Mont-2B'),
    ('Mont-2C'),
    ('Mont-2D'),
    ('Alto Agordino'),          
    ('Medio-Basso Agordino'),
    ('Cadore'),
    ('Feltrino-Val Belluna'),
    ('Altopiano dei sette comuni');

INSERT INTO Risk (risk_name) VALUES     -- risks
    ('idraulico'),
    ('idrogeologico'),
    ('idrogeologico con temporali'),
    ('nevicate');

INSERT INTO Role (role_name) VALUES     -- roles for the Users  
    ('normal'),
    ('admin'),
    ('super-admin');

INSERT INTO Color (color_name) VALUES       -- Color of every risk
    ('verde'),
    ('gialla'),
    ('arancione'),
    ('rossa');

INSERT INTO Altitude (height) VALUES        -- height for snow criticalness
    ('1000'),
    ('1500'),
    ('>1500'),
    ('2000'),
    ('>2000');






