# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

# We work with a dataframe called subdf
# DF will be the dataframe obtainedfrom submission.txt

# Processing times
year = subdf['DATE'].astype(str).str[:4].as_matrix()
month = subdf['DATE'].astype(str).str[5:7].as_matrix()
day = subdf['DATE'].astype(str).str[8:10].as_matrix()
slot = subdf['DATE'].astype(str).str[11:16].as_matrix()
hour = subdf['DATE'].astype(str).str[11:13].as_matrix()
halfh = subdf['DATE'].astype(str).str[14:16].as_matrix()

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
    date0[col] = np.zeros(len(subdf));
    
# ------------ At this point, you have all the discrete columns you need. Now you need to fill them ----------------


# Filling time discretisation dataframe
for i in range(len(subdf)):
    y = 'Y' + year[i];
    m = 'M' + month[i];
    d = 'D' + day[i];
    s = 'S' + slot[i];
    # wd = 'D' + subdf.DAY_WE_DS[i] #Will be useful to fill the weekdays
    l= [y,m,d,s,wd]
    for st in l:
        date0.loc[i,l]=1

# Append discretisation columns to data
subdf1 = pd.concat([date0,subdf],axis=1)


