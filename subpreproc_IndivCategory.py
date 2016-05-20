import pandas as pd
import numpy as np



def createTestFile_Indiv():
    
    
    submission = pd.read_csv('C:/Users/Ferdinand/Documents/Cours/Polytechnique Cours/3A/INF/INF582 Machine Learning/Axa Data Challenge/submission.txt',
                            sep='\t', parse_dates=['DATE'], dayfirst=True, 
                            index_col='DATE', nrows = 100)
        
        
    submission['DAY'] = submission.index.day
    submission['MONTH'] = submission.index.month
    submission['YEAR'] = submission.index.year
    submission['HOUR'] = submission.index.hour
    submission['MINUTE'] = submission.index.minute
    submission.index = range(len(submission))
                    
    # Remplissage a la main des features                
    dicday={'1': [0,0, 'Mardi'],
    '2': [0,0, 'Mercredi'],
    '3': [0,0, 'Lundi'],
    '4': [0,0, 'Lundi'],
    '5': [0,1, 'Samedi'],
    '6': [0,0, 'Lundi'],
    '7': [0,1, 'Dimanche'],
    '8': [0,0, 'Mardi'],
    '9': [0,0, 'Jeudi'],
    '10': [0,0, 'Mercredi'],
    '11': [0,0, 'Lundi'],
    '12': [0,0, 'Vendredi']}
    
    #Creation des colonnes                         
    submission['DAY_OFF']=0
    submission['WEEK_END']=0
    submission['DAY_WE_DS']=0
                             
    submission['Lundi']=0
    submission['Mardi']=0
    submission['Mercredi']=0
    submission['Jeudi']=0
    submission['Vendredi']=0
    submission['Samedi']=0
    submission['Dimanche']=0
                             
    asses = ['Téléphonie',
             'Finances PCX',
             'RTC',
             'Gestion Renault',
             'Nuit',
             'Gestion - Accueil Telephonique',
             'Regulation Medicale',
             'Services',
             'Tech. Total',
             'Gestion Relation Clienteles',
             'Crises',
             'Japon',
             'Médical',
             'Gestion Assurances',
             'Domicile',
             'Gestion',
             'SAP',
             'Medicine',
             'LifeStyle',
             'Technical',
             'TAI - RISQUE SERVICES',
             'RENAULT',
             'TAI - CARTES',
             'TAI - SERVICE',
             'TAI - RISQUE',
             'TAI - PNEUMATIQUES',
             'Gestion Amex',
             'Maroc - Génériques',
             'TPA',
             'Tech. Inter',
             'A DEFINIR',
             'Technique Belgique',
             'Technique International',
             'Gestion Clients',
             'Manager',
             'Tech. Axa',
             'DOMISERVE',
             'Truck Assistance',
             'NL Technique',
             'Réception',
             'CAT',
             'Gestion DZ',
             'NL Médical',
             'Mécanicien',
             'TAI - PANNE MECANIQUE',
             'FO Remboursement',
             'CMS',
             'Maroc - Renault',
             'Divers',
             'Prestataires',
             'AEVA',
             'Evenements',
             'KPT',
             'IPA Belgique - E/A MAJ',
             'Juridique']
        
        
        #########################################
    
    # Remplissage colonnes avec le dictionnaire manuel    
    dayoff = lambda x: dicday.get(str(x))[0]
    weekend = lambda x: dicday.get(str(x))[1]
    dayweds = lambda x: dicday.get(str(x))[2]
                    
    submission[['DAY_OFF']] = submission['MONTH'].apply(dayoff)
    submission[['WEEK_END']] = submission['MONTH'].apply(weekend)
    submission[['DAY_WE_DS']] = submission['MONTH'].apply(dayweds)
                                
    # Remplissage colonne week days                            
    weekdays=['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
    for wd in weekdays:
        submission.loc[np.array(submission['DAY_WE_DS'] == wd),wd] = 1
             
    # Creation colonnes Assignment
    for ass  in asses:
        submission[ass]=0

    assesloc = submission['ASS_ASSIGNMENT'].unique()
    
    # Filling assignments columns
    for ass in assesloc:
        submission.loc[np.array(submission['ASS_ASSIGNMENT'] == ass),ass] = 1
    
    # On utilise split_cods_str calcule dans natferpreproc_IndivCategory
    # split_cods_str = ['SPLIT_1', 'SPLIT_2',..., 'SPLIT_1591'] all the split cods are there
    # split dic = {'CAT':['SPLIT_15', 'SPLIT_18', ..], 'Telephonie':['SPLIT_25',...], ...}
        # associates ASSIGNMENT with all the possible SPLIT_CODS
      
    #Creating SPLIT_CODS columns in submission   
    nonsplit_cols = submission.columns.values.tolist()    
    for col in split_cods_str:
        submission[col] = 0
    
    # Methode bourring: On boucle sur tous les SPLIT_CODS pour le filling. 
    # Meilleure methode ci-dessous: boucler sur les SPLIT_CODS du dictionnaire en rentrant la cle ASSIGNMENT
    # submission['SPLIT_LIST']=0
    # for ass in asses:
    #    submission.loc[submission['ASS_ASSIGNMENT'] == ass,'SPLIT_LIST'] = splitdic[ass]
    #    split_arr = np.array(split_list)
    #    submission.loc[submission['ASS_ASSIGNMENT'] == ass,split_arr] = 1   
    
    # Filling des colonnes SPLIT adapte a chaque ASSIGNMENT
    # On utilise split_cods_str et splitdic calcule dans natferpreproc_IndivCategory
    for ass in asses:
        split_list = splitdic[ass]
        split_arr = np.array(split_list)
        submission.loc[submission['ASS_ASSIGNMENT'] == ass,split_arr] = 1     
    
    # Auto-fill SPLIT Columns --- Methode boucle sauvage - Ne FOnctionne PAS
    #submission_long = pd.DataFrame()
    #sub_cols = submission.columns.values.tolist()
    #for col in sub_cols:
    #    submission_long[col]=0
    #j=0
    #for i in range(len(submission)):     
    #    splist = splitdic[submission.loc[i,'ASS_ASSIGNMENT']]
    #    for split in splist:
    #        if (submission.loc[i,split] == 1):
    #            newline = submission0.iloc[i]
    #            newline[split] = 1
    #            submission_long.loc[j]=newline
    #            j = j+1
    
    # Auto-fill SPLIT Columns
    # Solution Giatsidis
    # Here we add one row for every SPLIT_COD of a given ASSIGNMENT
    # The rows added are sparse : 1 in the corresponding SPLIT, 0 in other SPLIT_CODS
    submission_long = pd.DataFrame()
    for split in split_cods_str:
        nonsplit_cols.append(split)
        submission_long = pd.concat([submission_long,submission.loc[submission[split] == 1 ,nonsplit_cols]],axis = 0)
        nonsplit_cols.remove(split)
    submission_long = submission_long.fillna(0)

    # Reordering
    newcols=['YEAR','MONTH','DAY','HOUR','MINUTE','Lundi','Mardi','Mercredi',
    'Jeudi','Vendredi','Samedi','Dimanche','DAY_OFF','WEEK_END']
    for ass in asses:
        newcols.append(ass)
    newcols = newcols + split_cods_str
    
    newcols.append('prediction')
    submission = submission[newcols]
    
#================ test set ============
    xtest= submission.drop('prediction',axis=1)
    
    
    return xtest





def CreatePredFile(ypredict):    
    
    submit = pd.read_csv('submission.txt', sep='\t')    
    
    mysub = open("mysub.txt", "w")
    mysub.write('DATE'+'\t'+'ASS_ASSIGNMENT'+'\t'+'prediction'+'\n')
    
    cpt = 0
    while cpt<12408:
        stringo=str(submit['DATE'][cpt])+'\t'+str(submit['ASS_ASSIGNMENT'][cpt])+'\t'+str(ypredict[cpt])+'\n'
        mysub.write(stringo)
        cpt+=1
    
    mysub.close()
    

def CreatePredFile_Indiv(xtest, ypredict):    
    
    xtest['prediction_indiv'] = ypredict
    
    asses = ['Téléphonie',
             'Finances PCX',
             'RTC',
             'Gestion Renault',
             'Nuit',
             'Gestion - Accueil Telephonique',
             'Regulation Medicale',
             'Services',
             'Tech. Total',
             'Gestion Relation Clienteles',
             'Crises',
             'Japon',
             'Médical',
             'Gestion Assurances',
             'Domicile',
             'Gestion',
             'SAP',
             'Medicine',
             'LifeStyle',
             'Technical',
             'TAI - RISQUE SERVICES',
             'RENAULT',
             'TAI - CARTES',
             'TAI - SERVICE',
             'TAI - RISQUE',
             'TAI - PNEUMATIQUES',
             'Gestion Amex',
             'Maroc - Génériques',
             'TPA',
             'Tech. Inter',
             'A DEFINIR',
             'Technique Belgique',
             'Technique International',
             'Gestion Clients',
             'Manager',
             'Tech. Axa',
             'DOMISERVE',
             'Truck Assistance',
             'NL Technique',
             'Réception',
             'CAT',
             'Gestion DZ',
             'NL Médical',
             'Mécanicien',
             'TAI - PANNE MECANIQUE',
             'FO Remboursement',
             'CMS',
             'Maroc - Renault',
             'Divers',
             'Prestataires',
             'AEVA',
             'Evenements',
             'KPT',
             'IPA Belgique - E/A MAJ',
             'Juridique']    
    
    # Gouping by sum the different SPLIT_CODS for each ASSIGNMENT x Date
    unique_cols = ['YEAR','MONTH', 'DAY','HOUR','MINUTE','Lundi' ,'Mardi', 
               'Mercredi' ,'Jeudi' ,'Vendredi' ,'Samedi', 'Dimanche' , 'DAY_OFF',
               'WEEK_END','ACD_COD'] # cols used for the grouping
    unique_cols = unique_cols + asses
    xtest_agg = xtest.groupby(unique_cols, as_index=False)
    xtest_agg = xtest_agg.aggregate(np.sum)
    
    # Sorting to match order of submission.txt
    xtest_agg.sort(['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'ASSIGNMENT'])
    
    # Extracting prediction
    ypredict2 = xtest_agg['prediction_indiv']
    
    # Calling previous CreatePredFile function
    return CreatePredFile(ypredict2)


