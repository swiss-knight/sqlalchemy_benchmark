#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 18:45:45 2023

@author: swiss_knight
"""

import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
from sqlalchemy import create_engine, text

def foo():
    engine = create_engine("postgresql://postgres:password@db:5432/postgres")
    with engine.begin() as connection:
        gdf0 = gpd.read_postgis(
            sql = text("WITH cte AS (SELECT * FROM public.cities) SELECT *, ST_Buffer(geom,0.0001) FROM public.cities WHERE name ILIKE 'bog';"),
            con=connection,
            geom_col='geom',
            crs=4326,
        )
        gdf1 = gpd.read_postgis(
            sql = text("WITH cte AS (SELECT * FROM public.cities) SELECT *, ST_Buffer(geom,0.0002) FROM public.cities WHERE name ILIKE 'bra';"),
            con=connection,
            geom_col='geom',
            crs=4326,
        )
        gdf2 = gpd.read_postgis(
            sql = text("WITH cte AS (SELECT * FROM public.cities) SELECT *, ST_Buffer(geom,0.0003) FROM public.cities WHERE country ILIKE 'ven';"),
            con=connection,
            geom_col='geom',
            crs=4326,
        )

i=-1
while i < 100:
   i+=1
   foo()
