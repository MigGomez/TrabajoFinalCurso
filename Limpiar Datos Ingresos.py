import pandas as pd
import numpy as np
from fuzzywuzzy import process
from datetime import date

today = date.today()

df_dic = pd.read_excel('Diccionario de datos/dic_nombreCine.xlsx')
paises = ['El Salvador','Guatemala', 'Honduras', 'Nicaragua', 'Panama', "Costa Rica"]
df_titulos = pd.read_excel('Diccionario de datos/dic_Titulos.xlsx')
titulos=[]

for p in paises:
    df = pd.read_excel('Datos Ingresos/'+p+'.xls')
    df = df.drop(df.index[0])
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])
    
    if p == 'Nicaragua':
        df['Circuit'] = df['Circuit'].replace(['Diusa'], 'Cinemas')
    
    cine = df['Circuit'].unique()
    
    for i in cine:
        if i !='Cinemark' and i != 'Cinepolis' and i != 'Cinemas':
            indexNames = df[df['Circuit']==i].index
            df.drop(indexNames , inplace=True)
    
    mal = df['Theatre Name'].unique()
    bien = df_dic[df_dic['Pais']==p] ['Nombre Cine'].unique()
    
    for i in mal:
        x = process.extractOne(i, bien)

        if x[1]>=50:
            df['Theatre Name'] = df['Theatre Name'].replace([i], x[0])
            
    df = df.rename(columns={'Theatre Name':'Nombre Cine','Title':'Titulo','City':'Ciudad','Circuit':'Cine'})
    
    titulos.extend(df['Titulo'].unique())
    
    df.to_excel('Data Transformation/'+p+'.xlsx', index=False)
    
for c in paises:
    df = pd.read_excel('Data Transformation/'+c+'.xlsx')
    
    for i in list(df):
        if "%" in i:
            df = df.drop([i], axis=1)
        elif "mf_" in i:
            df = df.drop([i], axis=1)
        elif "Week" in i:
            df = df.drop([i], axis=1)
        elif "Rank" in i:
            df = df.drop([i], axis=1)
        elif "Rtk" in i:
            df = df.drop([i], axis=1)

    df.to_excel('Data Transformation/'+c+'.xlsx', sheet_name=c, index=False)
   
df_t = pd.DataFrame(titulos)
df_t = df_t.drop_duplicates()
df_titulos = pd.concat([df_titulos, df_t], axis=0)
df_titulos = df_titulos.drop_duplicates()

df_titulos.to_excel('Diccionario de datos/dic_Titulos.xlsx',  index=False)