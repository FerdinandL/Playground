# -*- coding: utf-8 -*-
"""
Avec ca tu pourras process le df de base pour arriver a quelquechose sur lequel tu peux train les modeles
Les modeles vont mettre pas mal de temps a fitter le dataset peut etre, have fun!
"""

import pandas as pd
import numpy as np

# Import tables
df = pd.read_csv('train_2011_2012.csv', sep=';')

# Processing times
year = df['DATE'].astype(str).str[:4].as_matrix()
month = df['DATE'].astype(str).str[5:7].as_matrix()
day = df['DATE'].astype(str).str[8:10].as_matrix()
slot = df['DATE'].astype(str).str[11:16].as_matrix()

# Date0 will contain all the discrete columns used to discretize time
date0 = pd.DataFrame()

# Discrete columns names 
# One columns per year, per month, per day, per 30-min slot
newcols=['Y2011','Y2012','M01','M02','M03', 'M04', 'M05', 'M06', 'M07', 
'M08', 'M09', 'M10', 'M11', 'M12']
for i in range(1,32):
    if (i<10):
        newcols.append('D0'+str(i))
    else:
        newcols.append('D'+str(i))
        
# One column per week day
dlist = ['DLundi','DMardi', 'DMercredi', 'DJeudi', 'DVendredi', 'DSamedi', 'DDimanche']
for k in dlist:
    newcols.append(k)

for i in range(48):
    if (int(i/2)<10):
        j= '0' + str(int(i/2))
    else:
        j= str(int(i/2))
    if (i % 2 == 1):
        newcols.append('S' + j + ':30') 
    else:
        newcols.append('S' + j + ':00')
        
# Empty discrete colums
for col in newcols:
    date0[col] = np.zeros(len(df));


# ------------ At this point, you have all the discrete columns you need. Now you need to fill them ----------------


# Filling time discretisation dataframe
for i in range(len(df)):
    y = 'Y' + year[i];
    m = 'M' + month[i];
    d = 'D' + day[i];
    s = 'S' + slot[i];
    wd = 'D' + df.DAY_WE_DS[i]
    l= [y,m,d,s,wd]
    for st in l:
        date0.loc[i,l]=1

# Append discretisation columns to data
df1 = pd.concat([date0,df],axis=1)

# ==== First very naive model: random forest keeping discrete date/time, weekends & off-days
# & ASS_ASSIGNMENT, CSPL_RECEIVED_CALLS =========

# We only keep the columns we need
df1_col = df1.columns.values.tolist()
df2_col = df1_col[0:(df1_col.index('DATE')+1)]
df2_col.extend(('DAY_OFF', 'WEEK_END', 'ASS_ASSIGNMENT'))
df2_col_unique = df2_col.copy()
df2_col.append('CSPL_RECEIVED_CALLS')
df2 = df1.loc[:,df2_col]


# Groupby : sum CSPL_RECEIVED_CALLS by (ASS_ASSIGNMENT and DATE)
df2g = df2.groupby(df2_col_unique, as_index=False)
df2g = df2g.aggregate(np.sum)


#================= Done!  =====================
# You can train models on this data set
# Here a sample of how to train : 

# Before what is below : split in train / test datasets
# After this:

reglin = linear_model.LinearRegression()
reglin.fit(df_data,df_target)
ypredict=reglin.predict(test_data)
mse_linreg = mean_squared_error(test_target, ypredict)
print(mse_linreg)
# There are also function which can do this automatically: check doc of cross_validation for
    # auto parition train / test
    # auto fit on train and auto mse on tes

# For next step, CV technique:
#Cross validation and mean score - It may be costly so useless now
reglin = linear_model.LinearRegression()
scores = cross_validation.cross_val_score(reglin,s15p1a_train_data, s15p1a_train_target, scoring='mean_squared_error', cv=5)
print(scores.mean())
print(scores)
