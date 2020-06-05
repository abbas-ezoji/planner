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
HOST = '.'
PORT = '1433'
NAME = 'planning'
engine = create_engine('mssql+pyodbc://{}:{}@{}/{}?driver=SQL+Server' \
                       .format(USER,
                               PASSWORD,
                               HOST,
                               NAME
                               ))
    
cities = pd.read_sql_query('''select 
									id
								from
									plan_city
								where id not in
											(select  city_id	
											from
												plan_attraction a join plan_distance_mat m on m.origin_id = a.id
												)
									 and id !=39
                                ''',
                       con=engine)
cities =np.array(cities.values, dtype = int)
for city in cities:
    attraction = pd.read_sql_query('''SELECT 
                                              city_id, id, latt, long
                                      FROM [plan_attraction]
                                      where city_id  = {}
                                    '''.format(city[0]),
                           con=engine)
    
    dist_matrix = []
    for i,a in enumerate(attraction.iterrows()):
        city = (attraction.iloc[i,0])
        orig_id = (attraction.iloc[i,1])
        orig_latt = (attraction.iloc[i,2])
        orig_long = (attraction.iloc[i,3])
        destinations = attraction[attraction['city_id']==city]
        print('city: ' + str(city) + ' from ' + str(orig_id) + ' to ' )
        
        for j,d in enumerate(destinations.iterrows()):
            dest_id = (attraction.iloc[j,1])
            dest_latt = (attraction.iloc[j,2])
            dest_long = (attraction.iloc[j,3])
            print('dest: ' + str(dest_id))
    
            url = 'https://api.neshan.org/v2/direction?'
            apiKey = 'service.rstJXLArDfrfB3GG2iLd3i08trxmzNP1gjKd4lEI'
            origin = str(orig_latt) + ',' + str(orig_long)
            destin = str(dest_latt) + ',' + str(dest_long)
    
            url = url + 'origin=' + origin + '&destination=' + destin
            headers = {"Accept": "application/json", "Api-Key":apiKey}
            r = requests.get(url, headers = headers)
            data = r.json() 
            
            try:
                route = data['routes'][0]['legs'][0]
                len_time = route['duration']['value']//60
                len_meter = route['distance']['value']
                
                ecl_dist = math.sqrt((orig_latt-dest_latt)**2 + (orig_long-dest_long)**2)        
                destination_id = dest_id
                origin_id = orig_id
                travel_type_id = 1
                
                dist_matrix.append([ecl_dist, len_meter, len_time, 
                                origin_id, destination_id, 
                                travel_type_id, route])
            except:
                dist_matrix.append([-1, -1, -1, 
                                orig_id, dest_id, 
                                1, ''])
            
            # query = '''update [plan_distance_mat]
            #            set ecl_dist = {}, len_meter = {}, len_time = {}, 
            #               travel_type_id = {}, route = {}
            #            where origin_id = {} and destination_id = {}
            #         '''.format(ecl_dist, len_meter, len_time, 
            #                    travel_type_id, "''",
            #                    origin_id, destination_id)        
            # with engine.connect() as con:
            #     con.execute(query)
            
    print('insert into db for city: ' + str(city))
    with engine.connect() as con:
        for i,d in enumerate(dist_matrix):
            query = '''insert into [plan_distance_mat] values({}, {}, {}, 
                                                        {}, {}, {}, {})
                    '''.format(d[0], d[1], d[2], d[3], d[4], d[5], "''")
            con.execute(query)
            route_query = '''insert into [plan_dist_mat_routes] values({}, {}
                            , {}, {})
                    '''.format("'"+str(d[6]).replace("'",'"')+"'", 0, d[3], d[4])
            con.execute(route_query)
    print('finish')
