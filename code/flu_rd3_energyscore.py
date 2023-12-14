import pandas as pd
import numpy as np
import datetime
from scorepi import *
from epiweeks import Week
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns
import datetime
from datetime import datetime
from datetime import timedelta
from pathlib import Path
import matplotlib as mpl
import random
import sys
#from numba import njit
from energyscore_fcn import energyscore


import warnings
warnings.filterwarnings('ignore')


locations = pd.read_csv('./locations.csv',dtype={'location':str})
predictionsall = pd.read_pickle('./fludat/trajectories_SMHrd3.pkl')

# lump all trajectories to together - this forms the ensemble model


# raw score

rd =17 
start_week = Week(2023, 16)
max_date = pd.to_datetime('2023-09-01')

#loclist = list(predictions.location.unique())
#loclist.remove('US')

energyscoresdf = pd.DataFrame()


loclist = list(predictionsall.location.unique())
loclist.remove('US')

predictionsall = predictionsall.drop_duplicates()

for model in predictionsall.Model.unique():
    for loc in ['US']:
        
        for scenario in ['A', 'B', 'C', 'D', 'E', 'F']:
            location = loc
            target = 'hosp'
            incidence = True

            if target == 'hosp':
                target_obs = 'hospitalization'
            else:
                target_obs = target_obs
                
            

            observations = pd.read_parquet(f"./fludat/truth_{'inc' if incidence else 'cum'}_{target_obs}.pq")
            observations['date'] = pd.to_datetime(observations['date'])

            target_prediction_list = [f"{i} wk ahead {'inc' if incidence else 'cum'} {target}" for i in range(1,100)]

            predictionsfilt = predictionsall[(predictionsall.scenario_id == scenario + '-2022-12-04') & \
                                        (predictionsall.location == location) & \
                                        (predictionsall.Model == model) & \
                                        (predictionsall.target.isin(target_prediction_list))  & \
                                        (predictionsall.target_end_date <= observations.date.unique().max()) & \
                                        (predictionsall.target_end_date >= pd.to_datetime(start_week.startdate()))]

        
            #for i in [predictionsfilt.type_id.unique()[0]]:
            #    pfilt = predictionsfilt[predictionsfilt.trajectory_id == i]


            observations = observations[(observations['date'] >= pd.to_datetime(start_week.startdate())) & \
                                        (observations['date'] <= predictionsfilt.target_end_date.unique().max())]   

            #filter location
            observations = observations[observations['location'] == location]

            #aggregate to weekly
            observations = observations.groupby(['location', pd.Grouper(key='date', freq='W-SAT')]).sum().reset_index()

            #transform to Observation object
            observations = Observations(observations)


            y = np.array(observations.value)
            X = [np.array(predictionsfilt[predictionsfilt['sample'] == i].value) for i in predictionsfilt['sample'].unique()]

            ES = energyscore(np.array(X),y)
            
            

            #energyscores[loc][scenario] = ES

            if loc == 'US':
                loc_conv = loc
            elif int(loc) <10:
                loc_conv = loc[1]
            else:
                loc_conv = loc  

            newrow = pd.DataFrame({'Model':model,'Label': 'Scenario '+ scenario, 'location':loc_conv, 'energyscore':ES, 
                                'target':target}, index=[0])

            energyscoresdf = pd.concat([energyscoresdf, newrow])

energyscoresdf = energyscoresdf.reset_index()
energyscoresdf = energyscoresdf.drop(columns=['index'])   


energyscoresdf = pd.merge(energyscoresdf, locations, how = 'inner', on = 'location')



energyscoresdf.to_pickle(f'./energyscore_models_flurd3_hosp.pkl')

print('done')




