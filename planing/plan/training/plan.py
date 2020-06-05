###############################################################################
'''                     Author: Abbas Ezoji
                     Email: Abbas.ezoji@gmail.com
'''
###############################################################################
import pandas as pd
import numpy as np
import numpy_indexed as npi
import uuid
import random
import pyodbc
import math
import clustering
from ga_numpy import GeneticAlgorithm as ga
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from time import gmtime, strftime

###############################################################################
'''                             parameters                            '''
###############################################################################
city = 1
start_time = 420
end_time = 1440 
days = 2

population_size = 50
generations = 200

coh_pnlty = 10

coh_fultm = 0.8
coh_dffRqTime  = 0.1
coh_dffVisTime  = 0.1

coh_lntm  = 0.4
coh_cnt   = 0.05
coh_rate = 0.55

###############################################################################
'''                  Cost calculation functions                             '''
###############################################################################
def cost_fulltime(individual, end_plan):      
    cost = np.abs(end_plan  - end_time) / (end_time - start_time)
      
    return cost

def cost_lentime(individual, all_dist, all_duration):         
    cost = all_dist / (all_duration + all_dist)
      
    return cost
	
def cost_count(individual, meta_data):
    plan = individual
    len_pln = len(plan)
    len_points = len(meta_data)
    cost = np.abs(len_points - len_pln) / len_points
    
    return cost

def cost_diffTime(individual):
    plan = individual
    max_rqTime = np.max(plan[:,7])     
    max_visTime = np.max(plan[:,6]) - np.min(plan[:,5])
            
    rq_time  = np.apply_along_axis(apply_rqTime, 1, plan)    
    vis_time = np.apply_along_axis(apply_visTime, 1, plan)
    
    plan[:,8] = rq_time
    plan[:,9] = vis_time

    cost_vis_time = np.sum(vis_time) / max_rqTime
    cost_rq_time = np.sum(rq_time) / max_visTime   
    
    return cost_vis_time, cost_rq_time

def cost_rate(individual, meta_data):
    plan = individual
    max_rate = np.max(meta_data[:,10])
    min_rate_plan = np.min(plan[:,10])
    max_rate_plan = np.max(plan[:,10])

    diff_range = max_rate - min_rate_plan
    len_pln = len(plan)
    
    chebi_cost = (max_rate - max_rate_plan)/diff_range
    norm_cost = np.sum(max_rate - plan[:,10])/(len_pln*diff_range)
    cost = np.sum([chebi_cost,norm_cost])
    
    return cost

###############################################################################
'''               individual General functions                          '''
###############################################################################
def set_const(individual, const):
    for c in const:
        msk = np.logical_and(individual[:,3]>=c[5], individual[:,3]<=c[6])        
        p = individual[msk]
        if len(p)>0:
            min_p = np.min(p[:,3]) 
            p = p[p[:,3]==min_p]
            c[3] = p[0,3]
            # individual[individual[:,3]==p[:,3]] = c
            individual = np.vstack([individual, c])
            
            #print(len(individual))
        else:
            nearest_dist = np.min(np.abs(individual[:,3] - c[5]))
            msk1 = np.abs(individual[:,3] - c[5])==nearest_dist
            msk2 = individual[:,2]==0
            p = individual[np.logical_and(msk1,msk2)]
#            print(p)
            if len(p)>0:
                min_p = np.min(p[:,3]) 
                p = p[p[:,3]==min_p]
                c[3] = p[0,3]
                # individual[individual[:,3]==p[:,3]] = c
                individual = np.vstack([individual, c])
            else:
                c[3] = c[5]
                individual = np.vstack([individual, c])

    individual = individual[np.lexsort((-individual[:,2], individual[:,3]))]
        
    return individual
    
def calc_starttime(individual): 
    pln_pnt = individual[:,0]
    # individual = individual[np.lexsort((individual[:,3], -individual[:,2]))]
    for i,dist in enumerate(pln_pnt):
        if i==0:
            individual[i,3] = start_time
        elif individual[i-1,2] == 0 and individual[i,2] == 0: # if last and current type not const
            individual[i,4] = dist_mat.loc[pln_pnt[i-1], pln_pnt[i]]
            individual[i,3] = individual[i,4] + individual[i-1,3] + individual[i-1,1]
        elif individual[i-1,2] > 0 or individual[i,2] > 0:
            individual[i,3] = individual[i-1,3] + individual[i-1,1]
    
    return individual

def apply_visTime(a):
    start = a[3]
    end = a[3] + a[1]
    vis_time  = a[5] - start if a[5]>start else 0
    if a[6]!=0:
        vis_time += end - a[6]   if end>a[6] else 0    
    
    return vis_time

def apply_rqTime(a):    
    
    return np.abs(a[1]-a[7])

###############################################################################
'''                  Cost fitness totla function                            '''
###############################################################################
def fitness(individual, meta_data):    
    _, individual = npi.group_by(individual[:,0]).max(individual)
    
#    individual = set_const(individual, const)
    calc_starttime(individual)
    individual = set_const(individual, const)
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
    cost_vis_time, cost_rq_time = cost_diffTime(individual)
    cost_rte   = cost_rate(individual, meta_data)
    
    # print('cost_fultm: '+str(cost_fultm))
    # print('cost_lntm: '+str(cost_lntm))
    # print('cost_cnt: '+str(cost_cnt))
    # print('cost_vis_time: '+str(cost_vis_time))
    # print('cost_rte: '+str(cost_rte))
    
    cost =((coh_rate*cost_rte)+
           (coh_cnt*cost_cnt)+
           (coh_lntm*cost_lntm))
           
#    print(cost)

    penalty = ((coh_fultm*cost_fultm)+
               (coh_dffRqTime*cost_rq_time)+
               (coh_dffVisTime*cost_vis_time)) 
    
    # return cost + penalty
    return cost *(1 + (coh_pnlty*penalty))

###############################################################################
'''                             connection config                           '''
###############################################################################
USER = 'sa' # settings.DATABASES['default']['USER']
PASSWORD = 'xZCtQxjK3z9A' # settings.DATABASES['default']['PASSWORD']
HOST = '185.10.72.91,1886' # settings.DATABASES['default']['HOST']
PORT = '1433' # settings.DATABASES['default']['PORT']
NAME = 'planning' # settings.DATABASES['default']['NAME']

engine = create_engine('mssql+pyodbc://{}:{}@{}/{}?driver=SQL+Server' \
                       .format(USER,
                               PASSWORD,
                               HOST,                    
                               NAME
                               ))

###############################################################################
'''                             Fetch data from db                          '''
###############################################################################
df_city_total = pd.read_sql_query('''SELECT * FROM 
                          [planning]..plan_attraction WHERE type=0
                          AND city_id = {}'''.format(city),
                       con=engine)
df_city_total = df_city_total.drop(['fullTitle', 'address', 'description','image'], axis=1)

df_city_total['rate'] = df_city_total['iplanner_rate']*100

dist_mat_query = ''' SELECT 
                         origin_id as orgin
                        ,destination_id as dist
                        ,len_time as len
                     FROM 
                       plan_distance_mat
                     WHERE
                       origin_id in 
                       (SELECT id FROM plan_attraction
                        WHERE city_id = {0} AND type=0)
                       '''.format(city)
###############################################################################
'''                  Create dist_mat, Const and meta_data                   '''
#################''' Create distance matrix '''################################             
             
dist_df = pd.read_sql_query(dist_mat_query
                          ,con=engine)

dist_mat = pd.pivot_table(dist_df,                           
                          index=['orgin'],
                          columns=['dist'], 
                          values='len', 
                          aggfunc=np.sum)
######################''' Create Costraints '''################################             
                                        
const_df = pd.read_sql_query('SELECT * FROM plan_attraction WHERE type>0',
                             con=engine)

vst_time_from = np.array(const_df['vis_time_from'])
vst_time_to = np.array(const_df['vis_time_to'])
points = np.array(const_df['id'])
rq_time = np.array(const_df['rq_time'])
types = np.array(const_df['type'])
len_points = len(points)
rq_time_mean = np.min(rq_time)

const = np.array([points, 
                      rq_time, 
                      types, 
                      np.zeros(len_points),     # as strat time
                      np.zeros(len_points),     # as distance time
                      np.array(vst_time_from),  # as vst_time_from
                      np.array(vst_time_to),    # as vst_time_to
                      np.array(rq_time),        # as rq_time
                      np.zeros(len_points),     # as diff_rqTime
                      np.zeros(len_points),     # as diff_visTime
                      np.zeros(len_points),     # as rate
                      ],
                      dtype=int).T
                  
len_const = len(const) 
tot_lenTimeConst = np.sum(const[:,1]) 

#########''' Create all accepted Points as meta_data '''#######################                         
plan = []
train_time = gmtime()
time_str = str(train_time.tm_year) + '-' + \
           str(train_time.tm_mon) + '-' + \
           str(train_time.tm_mday) + '-' + \
           str(train_time.tm_hour) + '-' + \
           str(train_time.tm_min) + '-' + \
           str(train_time.tm_sec)
           
present_id = str(city) + '-' + str(days) + '-'  + time_str
last_plans = []

df_city_total = df_city_total.sort_values(by='iplanner_rate', ascending=False)



for day in range(1,days+1):
    if day>1:
        mask = ~df_city_total['id'].isin(last_plans[:,0])
        df_city = df_city_total[mask]
    else:
        df_city = df_city_total
        
    tot_lenTime = end_time - start_time
    rq_time_mean = np.sum(df_city['rq_time']*df_city['rate']) / np.sum(df_city['rate'])
    len_points = len(df_city)
    len_accpt_points = math.floor((tot_lenTime)/rq_time_mean)
    remainig_days = days - day + 1
    attr_divide = math.floor(len_points/len_accpt_points)
    if math.floor(attr_divide/day)>2:
        n_clusters = math.floor(attr_divide/day)
    else:
        n_clusters = 2

    X = np.array(df_city.loc[:,['id', 'iplanner_rate', 'latt', 'long']].values, 
             dtype=float)
    
    clustering.plot_2d(X)
    clustering.plot_3d(X)
    # n_clusters = days - day + 3
    random_state = day
    (cluster_labels, 
     cluster_centers, 
     max_cluster, 
     first_cluster_members) = clustering.kmeans_clsuster(X, n_clusters, 
                                                       random_state)

    # df_city = df_city.iloc[first_cluster_members,:]
    df_city = df_city.iloc[:len_accpt_points,:]
    
    df_city = df_city.sort_values(by='iplanner_rate', ascending=False)    
    
    points = np.array(df_city['id'])
    len_points = len(points)
    vst_time_from = np.array(df_city['vis_time_from'])
    vst_time_to = np.array(df_city['vis_time_to'])
    rq_time = np.array(df_city['rq_time'])  
    rate = np.array(df_city['rate']) 
    rq_time_mean = np.mean(rq_time)
    
    meta_data = np.array([points, 
                          rq_time, 
                          np.zeros(len_points),     # as zero as type
                          np.zeros(len_points),     # as strat time
                          np.zeros(len_points),     # as distance time
                          np.array(vst_time_from),  # as vst_time_from
                          np.array(vst_time_to),    # as vst_time_to
                          np.array(rq_time),        # as rq_time
                          np.zeros(len_points),     # as diff_rqTime
                          np.zeros(len_points),     # as diff_visTime
                          np.array(rate),           # as rate
                          ]).T

                    ###################################################
    '''                  Create sample gene from meta_data                  '''
                    ###################################################    
    np.random.shuffle(meta_data)
    
                    ###################################################
    '''                  Set parameters and Call GA                         '''
                    ###################################################
    if (day==1): # Definition GA object in first 
        ga = ga(seed_data=meta_data,
                meta_data=meta_data,    
                population_size=population_size,
                generations=generations,
                current_generation_count = 0,
                crossover_probability=0.8,
                mutation_probability=0.2,
                elitism=True,
                by_parent=False,
                maximise_fitness=False)	
        ga.fitness_function = fitness
    else:
        ga.set_data(seed_data = meta_data, meta_data = meta_data)
    ga.run()   
    
                    ###################################################
    '''                  Get GA outputs and calculate all cost and 
                         other output featurs      '''
                    ###################################################
    sol_fitness, sol_df = ga.best_individual()
    last_plans = sol_df if day==1 else np.concatenate((last_plans, sol_df), axis = 0)
    
    calc_starttime(sol_df)
    sol_df = set_const(sol_df, const)
    calc_starttime(sol_df)
    
    len_pln = len(sol_df)
    edge = len_pln - 1   
    pln_pnt = sol_df[:,0]
    len_points = len(points)
    all_duration = np.sum(sol_df[:,1])    
    end_plan = sol_df[edge,3]+sol_df[edge,1]
    all_dist = end_plan  - all_duration
        
    cost_fultm = cost_fulltime(sol_df, end_plan)
    cost_lntm  = cost_lentime(sol_df, all_dist, all_duration)
    cost_cnt   = cost_count(sol_df, meta_data)
    cost_vis_time, cost_rq_time = cost_diffTime(sol_df)
    cost_rte   = cost_rate(sol_df, meta_data)

    diff_full_time = end_plan - end_time
    
    cost =((coh_fultm*cost_fultm) + 
               (coh_lntm*cost_lntm) + 
               (coh_cnt*cost_cnt) + 
               (coh_dffRqTime*cost_rq_time)+
               (coh_dffVisTime*cost_vis_time)+
               (coh_rate*cost_rte)
               )    
    #    print(cost)
    
                    ###################################################
    '''                  Create query for inser plan in db                  '''
                    ###################################################  
    tags = 'test'
    comment = 'test'
    
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
                                           "cost_rate",
    									   start_time,
    									   end_time,
    									   dist_len,
    									   points_len,
    									   duration_len,
    									   tags,
    									   comment,
                                           day,
                                           "all_days")
                     values ({0}, {1}, 
                             {2}, {3}, {4}, {5},
                             {6}, {7}, {8}, {9},{10},
                             {11}, {12},
                             {13}, {14}, {15}, 
                             {16}, {17}, {18},{19}) 
                   '''.format(city, "'"+str(present_id)+"'",
                              coh_fultm, coh_lntm, coh_cnt, coh_dffRqTime, 
                              cost_fultm, cost_lntm, cost_cnt, cost_rq_time,cost_rte,
                              start_time, end_time,
                              all_dist, len_pln, all_duration,
                              "'"+str(tags)+"'", "'"+str(comment)+"'",
                              day, days
                              )
    
    engine.execute(query_plan)               
    
    inserted_plan = pd.read_sql_query('''SELECT * 
                                      FROM plan_plan
                                      WHERE present_id = {0} and day = {1}
                                          '''.format( "'"+str(present_id)+"'", day)
                                          ,con=engine)
    plan_id = int(inserted_plan['id'])
    
    for i, sol in enumerate(sol_df):
        qry = '''insert into 
                  plan_plan_details(plan_id, 
                                    "order",
                                    len_time,                              
                                    point_id,
                                    from_time,
                                    dist_to)
                  values({0}, {1}, {2}, {3}, {4}, {5})
                  '''.format(plan_id, i, sol[1], sol[0], sol[3], sol[4])
        engine.execute(qry)    


    last_gens = ga.last_generation()   

    last_genes = [gene.get_geneInfo() for gene in last_gens]
