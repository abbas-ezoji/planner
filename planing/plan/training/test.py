# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from ga_numpy_test import GeneticAlgorithm as ga
import numpy_indexed as npi
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
import uuid
import random


##############################
city = 36 
start_time = 480
end_time = 1440

coh_fultm = 0.6
coh_lntm  = 0.2
coh_cnt   = 0.05
coh_dffRqTime  = 0.15

#constraints = [[420,  540,  45, 1],    # breakfast time
#               [720,  960,  60, 2],    # lunch time
#               [1200, 1320, 50, 3],    # dinner time
#               [1380, 1440, 60, 4]]    # night sleep time
        
##############################
USER = 'planuser'
PASSWORD = '1qaz!QAZ'
HOST = 'localhost'
PORT = '5432'
NAME = 'planning'
db_connection = "postgresql://{}:{}@{}:{}/{}".format(USER,
                                                     PASSWORD,
                                                     HOST,
                                                     PORT,
                                                     NAME
                                                        )
engine = create_engine(db_connection)

df = pd.read_sql_query('SELECT * FROM	plan_attractions',con=engine)
df = df.drop(['image'], axis=1)

df_city = df[df['city_id']==city]

dist_mat_query = ''' select 
                         origin_id as orgin
                        ,destination_id as dist
                        ,len_time as len
                     from 
                       plan_distance_mat
                     where
                       origin_id in 
                       (select id from plan_attractions
                        where city_id = {0} and type=0)
                       '''.format(city)
             
dist_df = pd.read_sql_query(dist_mat_query
                          ,con=engine)

dist_mat = pd.pivot_table(dist_df,                           
                          index=['orgin'],
                          columns=['dist'], 
                          values='len', 
                          aggfunc=np.sum)

vst_time_from = np.array(df_city['vis_time_from'])
vst_time_to = np.array(df_city['vis_time_to'])
points = np.array(df_city['id'])
rq_time = np.array(df_city['rq_time'])
types = np.array(df_city['type'])
len_points = len(points)
rq_time_mean = np.min(rq_time)

len_accpt_points = (end_time - start_time)/rq_time_mean


meta_data = np.array([points, rq_time, types, np.zeros(len_points)], dtype=int).T

pln_gene1 = meta_data
np.random.shuffle(pln_gene1)

def calc_starttime(individual):
    plan = individual    
    pln_pnt = plan[:,0]
    for i,dist in enumerate(pln_pnt):  
        if i==0: 
            plan[i,3] = start_time       
        elif plan[i-1,2] == 0 and plan[i,2] == 0:
            plan[i,3] = dist_mat.loc[pln_pnt[i-1], pln_pnt[i]] + plan[i-1,3] + plan[i-1,1]
        else:
            plan[i,3] = plan[i-1,3] + + plan[i-1,1]
           
    return plan

#calc_starttime(pln_gene1)

def cost_fulltime(individual, end_plan):      
    cost = np.abs(end_plan  - end_time) / 1440.0     
      
    return cost

def cost_lentime(individual, all_dist, all_duration):         
    cost = all_dist / (all_duration + all_dist)
      
    return cost
	
def cost_count(individual, meta_data):
    plan = individual
    len_pln = len(plan)
    len_points = len(meta_data)
    cost = np.abs(len_accpt_points - len_pln) / len_points
    
    return cost

def cost_rqTime(individual, meta_data):
    plan = individual
   
    t = np.concatenate((plan, meta_data))
    _, t_max = npi.group_by(t[:,0]).max(t)
    _, t_min = npi.group_by(t[:,0]).min(t)
    t = (t_max - t_min)/t_max
    cost = np.sum(t[:,1]) / len(plan)   
    
    return cost

def fitness(individual, meta_data):    
    _, individual = npi.group_by(individual[:,0]).max(individual)
    
    calc_starttime(individual)
    len_pln = len(individual)
    edge = len_pln - 1   
    pln_pnt = individual[:,0]
    len_points = len(points)
    all_duration = np.sum(individual[:,1])    
    end_plan = individual[edge,3]+individual[edge,1]
    all_dist = end_plan  - all_duration
    
    cost_fultm = cost_fulltime(individual, end_plan)
    cost_lntm  = cost_lentime(individual, all_dist, all_duration)
    cost_cnt   = cost_count(individual, meta_data)
    cost_diff_rqTime = cost_rqTime(individual, meta_data)
#    print('cost_fultm: '+str(cost_fultm))
#    print('cost_lntm: '+str(cost_lntm))
#    print('cost_cnt: '+str(cost_cnt))
#    print('cost_diff_rqTime: '+str(cost_diff_rqTime))
#    
    cost =((coh_fultm*cost_fultm) + 
           (coh_lntm*cost_lntm) + 
           (coh_cnt*cost_cnt) + 
           (coh_dffRqTime*cost_diff_rqTime)
           )
#    print(cost)
    
    return cost

ga = ga(seed_data=pln_gene1,
        meta_data=meta_data,
        population_size=50,
        generations=200,
        crossover_probability=0.8,
        mutation_probability=0.2,
        elitism=True,
        by_parent=False,
        maximise_fitness=False)	
ga.fitness_function = fitness

ga.run()   

sol_fitness, sol_df = ga.best_individual()

individual = sol_df
calc_starttime(individual)
len_pln = len(individual)
edge = len_pln - 1   
pln_pnt = individual[:,0]
len_points = len(points)
all_duration = np.sum(individual[:,1])    
end_plan = individual[edge,3]+individual[edge,1]
all_dist = end_plan  - all_duration
    
cost_fultm = cost_fulltime(sol_df, end_plan)
cost_lntm  = cost_lentime(sol_df, all_dist, all_duration)
cost_cnt   = cost_count(sol_df, meta_data)
cost_diff_rqTime = cost_rqTime(sol_df, meta_data)
diff_full_time = end_plan - end_time
tags = 'test'
comment = 'test'
present_id = uuid.uuid1()
query_plan = '''insert into plan_plan (city_id,
									   present_id,
									   "coh_fullTime",
									   "coh_lengthTime",
									   "coh_countPoints",
									   "coh_minRqTime",
									   "cost_fullTime",
									   "cost_lengthTime",
									   "cost_countPoints",
									   "cost_minRqTime",
									   start_time,
									   end_time,
									   dist_len,
									   points_len,
									   duration_len,
									   tags,
									   comment)
                 values ({0}, {1}, 
                         {2}, {3}, {4}, {5},
                         {6}, {7}, {8}, {9}, 
                         {10}, {11},
                         {12}, {13}, {14}, 
                         {15}, {16}) 
               '''.format(city, "'"+str(present_id)+"'",
                          coh_fultm, coh_lntm, coh_cnt, coh_dffRqTime, 
                          cost_fultm, cost_lntm, cost_cnt, cost_diff_rqTime,
                          start_time, end_time,
                          all_dist, len_pln, all_duration,
                          "'"+str(tags)+"'", "'"+str(comment)+"'"
                          )

engine.execute(query_plan)               

inserted_plan = pd.read_sql_query('''SELECT * 
                                  FROM plan_plan
                                  WHERE present_id = {0}
                                  '''.format( "'"+str(present_id)+"'")
                                     ,con=engine)
plan_id = int(inserted_plan['id'])

for i, sol in enumerate(sol_df):
    qry = '''insert into 
             plan_plan_details(plan_id, 
                               "order",
                               len_time,                              
                               point_id,
                               from_date)
             values({0}, {1}, {2}, {3}, {4})
             '''.format(plan_id, i, sol[1], sol[0], sol[3])
    engine.execute(qry)
    

