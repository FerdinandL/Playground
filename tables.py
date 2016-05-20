# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys

# Clear all variables
sys.modules[__name__].__dict__.clear()

# Import tables
df = pd.read_csv('C:/Users/Ferdinand/Documents/Cours/Polytechnique Cours/3A/INF/INF582 Machine Learning/Axa Data Challenge/train_2011_2012.csv', sep=';',nrows = 100)

# Samples
df0 = df.iloc[np.random.permutation(len(df))]
df1 = df0[0:500000]
df2 = df0[0:100000]
df3= df0[0:10000]
df3.index = range(len(df3))

# Processing times
year = df3['DATE'].astype(str).str[:4].as_matrix()
month = df3['DATE'].astype(str).str[5:7].as_matrix()
day = df3['DATE'].astype(str).str[8:10].as_matrix()
slot = df3['DATE'].astype(str).str[11:16].as_matrix()

date0 = pd.DataFrame()

# Discrete columns names 
newcols=['Y2011','Y2012','M01','M02','M03', 'M04', 'M05', 'M06', 'M07', 
'M08', 'M09', 'M10', 'M11', 'M12']
for i in range(1,32):
    if (i<10):
        newcols.append('D0'+str(i))
    else:
        newcols.append('D'+str(i))
        
# Week days
dlist = ['Lundi','Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
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
    date0[col] = np.zeros(len(df3));


# Filling time discretisation dataframe
for i in range(len(df3)):
    y = 'Y' + year[i];
    m = 'M' + month[i];
    d = 'D' + day[i];
    s = 'S' + slot[i];
    wd = 'D' + df3.DAY_WE_DS[i]
    l= [y,m,d,s,wd]
    for st in l:
        date0.loc[i,l]=1
        
# Append discretisation columns to data
df4 = pd.concat([date0,df3],axis=1)

# First very naive model: random forest keeping discrete date/time, weekends & off-days
# ASS_ASSIGNMENT, CSPL_RECEIVED_CALLS
df4_col = df4.columns.values.tolist()
df5_col = df4_col[0:(df4_col.index('DATE')+1)]
df5_col.extend(('DAY_OFF', 'WEEK_END', 'ASS_ASSIGNMENT'))
df5_col_unique = df5_col.copy()
df5_col.append('CSPL_RECEIVED_CALLS')
df5 = df4.loc[:,df5_col]


# Groupby : sum CSPL_RECEIVED_CALLS over ASS_ASSIGNMENT and DATE
df5g = df5.groupby(df5_col_unique, as_index=False)
df5g = df5g.aggregate(np.sum)

#================= Process Data =====================


# 