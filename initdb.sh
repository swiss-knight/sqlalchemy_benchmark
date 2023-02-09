#!/bin/sh

psql -U postgres -d postgres -c "CREATE TABLE IF NOT EXISTS cities (
	id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	name text,
	country text,
	geom geometry(Point,4326)
);
INSERT INTO public.cities (name, country, geom)
VALUES 
('Buenos Aires', 'Argentina', ST_SetSRID(ST_Point(-58.66, -34.58), 4326)),
('Brasilia', 'Brazil', ST_SetSRID(ST_Point(-47.91,-15.78), 4326)),
('Santiago', 'Chile',  ST_SetSRID(ST_Point(-70.66, -33.45), 4326)),
('Bogota', 'Colombia', ST_SetSRID(ST_Point(-74.08, 4.60), 4326)),
('Caracas', 'Venezuela', ST_SetSRID(ST_Point(-66.86,10.48), 4326));"

