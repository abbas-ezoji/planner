from __future__ import unicode_literals
import pandas as pd
import numpy as np
import numpy_indexed as npi
import pyodbc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine,Table, Column, Integer, String, MetaData, ForeignKey
import uuid
import random
from hazm import *

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

df = pd.read_sql_query('SELECT * FROM safarzoon_attraction',con=engine)
df = df.drop(['image'], axis=1)

df_city = df

metadata = MetaData()
atttraction_tag = Table('safarzoon_attractions_tags', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('attractions_id', Integer),
                      Column('tags_id', Integer),
                    )

metadata.create_all(engine)

describtions = np.array(df_city.loc[:,['id', 'fullTitle', 'description','type']].values)
tags = pd.read_sql_query('SELECT id, title FROM plan_tags', con=engine)

data = []
for desc in describtions:
    if desc[3]>0:
        continue
    fulltile_txt = np.array(word_tokenize(desc[1]))
    description_txt = np.array(word_tokenize(desc[2]))
    fulltext = np.concatenate((fulltile_txt, description_txt))
    attarction_id = desc[0]    
    msk = np.isin(tags['title'],fulltext)
    tag_ids = tags[msk]['id']
    for tag_id in tag_ids:
        data.append([attarction_id, tag_id])        

with engine.connect() as con:
    for i,d in enumerate(data):
        query = 'INSERT INTO safarzoon_attractions_tags(attractions_id, tags_id) VALUES ({}, {})'.format(d[0], d[1])        
        con.execute(query)  







