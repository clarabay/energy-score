import pandas as pd
import numpy as np
import datetime
#from scorepi import *
#from epiweeks import Week
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns
import datetime
from datetime import datetime
from datetime import timedelta
from pathlib import Path
import matplotlib as mpl
import random
from numba import njit


@njit
def energyscore_multipletargets(X,y):
    # X is matrix of trajectories, y is observations
    ES = 0
    N = X.shape[0]
    for i in range(N):
        ES += np.sqrt(np.sum(((X[i]-y)/y)**2))/N
    for i in range(N):
        for j in range(N):
            ES -= np.sqrt(np.sum(((X[i]-X[j])/y)**2))/(2*N**2)
    return ES


dfall = pd.read_csv('./predictions_all_scenD.csv')
dfall['target_end_date'] = pd.to_datetime(dfall['target_end_date'])

#hospitalizations
target = 'hospitalization'
incidence=True
hosp = pd.read_parquet(f"./truth_{'inc' if incidence else 'cum'}_{target}.pq")
hosp['date'] = pd.to_datetime(hosp['date'])
hosp = hosp[(hosp.date>pd.to_datetime('2023-11-18'))].sort_values(by=['date']).reset_index().drop(columns=\
                                                                        ['Unnamed: 0', 'index','weekly_rate'])


energyscores_locall = pd.DataFrame()
for it in range(100):
    print(it)
    for model in ['MOBS_NEU-GLEAM_FLU']:
        #print(model)
        for scenario in ['D']:

            loc_array ={}
            j=0
            for loc in locations:
                if loc in ['72', '66', '69','60', '78']:
                    continue
                predictionshosp = dfall[(dfall.scenario_id == scenario + '-2023-08-14') & \
                                            (dfall.target_end_date <= hosp.date.max()) & \
                                            (dfall.target_end_date >= hosp.date.min())&\
                                            (dfall.Model == model) &\
                                            (dfall.location==loc)]
                hospfilt = hosp[hosp.location.isin(dfall[dfall.Model==model].location.unique())]
                obsnew = np.array([np.array(hospfilt[hospfilt.location == i].value) for \
                     i in hospfilt.location.unique()])
                

                newid = random.sample(list(predictionshosp['trajectory_id']), 
                                      k=len(list(predictionshosp['trajectory_id'])))
                predictionshosp['new_id'] = newid
                
                if len(predictionshosp)==0:
                    continue

                Xhosp = np.array([np.array(predictionshosp[predictionshosp.new_id == i].value) for \
                         i in predictionshosp.new_id.unique()])
                
                loc_array[loc] = Xhosp
                
                j+=1
                
            A = []
            for i in range(len(Xhosp)):
                B = []
                for loc in loc_array.keys():
                    if loc in ['72', '66']:
                        continue
                    if len(loc_array[loc]) ==0:
                        continue
                        
                    B.append(loc_array[loc][i])
                B = np.array(B)
                A.append(B)

            C = np.array(A)



            ES = energyscore_multipletargets(C,obsnew)


            newrow = pd.DataFrame({'Model':model , 'Label': 'Scenario '+ scenario, 
                                 'energyscore': ES, 'it':it}, index=[0])

            energyscores_locall = pd.concat([energyscores_locall, newrow])

energyscores_locall = energyscores_locall.reset_index().drop(columns=['index'])  

energyscores_locall.to_pickle(f'./ES_mt_locall_{model}')