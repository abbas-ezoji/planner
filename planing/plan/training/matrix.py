# -*- coding: utf-8 -*-
import math
import requests
import numpy as np
import pyodbc
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine,Table, Column, Integer, String, MetaData, ForeignKey

USER = 'sa'
PASSWORD = 'xZCtQxjK3z9A'
HOST = '185.10.72.91,1886'
PORT = '1433'
NAME = 'planning'
engine = create_engine('mssql+pyodbc://{}:{}@{}/{}?driver=SQL+Server' \
                       .format(USER,
                               PASSWORD,
                               HOST,
                               NAME
                               ))

df_attraction = pd.read_sql_query('''SELECT * FROM [plan_attraction]
                                ''',
                       con=engine)
attraction = df_attraction.loc[:,['city_id', 'id','latt', 'long']]

#data = pd.DataFrame([], columns=['ecl_dist', 'len_meter', 'len_time', 'origin_id', 'travel_type_id', 'rout'])
data = []
for i,a in enumerate(attraction):
    city = (attraction.iloc[i,0])
    orig_id = (attraction.iloc[i,1])
    orig_latt = (attraction.iloc[i,2])
    orig_long = (attraction.iloc[i,3])
    destinations = attraction[attraction['city_id']==city]
    print(len(destinations))
    
    for j,d in enumerate(destinations):
        dest_id = (attraction.iloc[j,1])
        dest_latt = (attraction.iloc[j,2])
        dest_long = (attraction.iloc[j,2])

        url = 'https://api.neshan.org/v2/direction?'
        apiKey = 'service.rstJXLArDfrfB3GG2iLd3i08trxmzNP1gjKd4lEI'
        origin = str(orig_latt) + ',' + str(orig_long)
        destin = str(dest_latt) + ',' + str(dest_long)

        url = url + 'origin=' + origin + '&destination=' + destin
        headers = {"Accept": "application/json", "Api-Key":apiKey}
        r = requests.get(url, headers = headers)
        data = r.json() 

        route = data['routes'][0]['legs'][0]
        len_time = route['duration']['value']//60
        len_meter = route['distance']['value']
        
        ecl_dist = math.sqrt((orig_latt-dest_latt)**2 + (orig_long-dest_long)**2)        
        destination_id = dest_id
        origin_id = orig_id
        travel_type_id = 1
        
        data.append([ecl_dist, len_meter, len_time, origin_id, 
                     travel_type_id, route])        

data        

