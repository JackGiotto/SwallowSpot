
INSERT INTO Area (area_name) VALUES     -- zone di rischio che dividono il veneto
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
    ('Alto Agordino'),          -- new areas from #56
    ('Medio-Basso Agordino'),
    ('Cadore'),
    ('Feltrino-Val Belluna'),
    ('Altopiano dei sette comuni');

INSERT INTO Risk (risk_name) VALUES
    ('idraulico'),
    ('idrogeologico'),
    ('idrogeologico con temporali'),
    ('nevicate');

INSERT INTO Role (role_name) VALUES
    ('normal'),
    ('admin'),
    ('super-admin');

INSERT INTO Color (color_name) VALUES
    ('verde'),
    ('gialla'),
    ('arancio'),
    ('rossa');






