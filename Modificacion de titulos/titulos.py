import pandas as pd
import numpy as np
from fuzzywuzzy import process
from datetime import date

today = date.today()

df_k = pd.read_excel('Data Collection/Cinemark - 28-08-2022.xlsx')
df_po = pd.read_excel('Data Collection/cinepolis - 28-08-2022.xlsx')
df_ms = pd.read_excel('Data Collection/cinemas - 28-08-2022.xlsx')

#Guardar las listas con los titulos
d1= df_k['Titulo'].unique()
d2= df_po['Titulo'].unique()
d3= df_ms['Titulo'].unique()

#Cambiar nombres de titulos de cinemark segun cinepolis
for i in d1:
    x = process.extractOne(i, d2)
    if x[1]>=60:
        df_k['Titulo'] = df_k['Titulo'].replace([i], x[0])
        
#actualizamos lista de titulos
d1= df_k['Titulo'].unique()

#cambiamos los nombres de cinepolis segun cinemark
for i in d2:
    x = process.extractOne(i, d1)
    if x[1]>=60:
        df_po['Titulo'] = df_po['Titulo'].replace([i], x[0])

#actualizamos lista d titulos
d2= df_po['Titulo'].unique()

#cambiamos los nombres de cinemas segun cinepolis
for i in d3:
    x = process.extractOne(i, d1)
    if x[1]>=60:
        df_ms['Titulo'] = df_ms['Titulo'].replace([i], x[0])        

#actualizamos
d3= df_ms['Titulo'].unique()

#Concatenamos para hacer una lista d los titulos
df1 = df_k[['Titulo']].drop_duplicates()
df2 = df_po[['Titulo']].drop_duplicates()
df3 = df_ms[['Titulo']].drop_duplicates()

df_dic = pd.concat([df1, df2, df3], axis=0)
df_dic = df_dic.drop_duplicates()

#Guardar ya con los titulos modificados
df_k.to_excel('Modificacion de titulos/archivos/Cinemark - '+today.strftime('%d-%m-%Y')+'.xlsx', index=False)
df_po.to_excel('Modificacion de titulos/archivos/Cinepolis - '+today.strftime('%d-%m-%Y')+'.xlsx', index=False)
df_ms.to_excel('Modificacion de titulos/archivos/Cinemas - '+today.strftime('%d-%m-%Y')+'.xlsx', index=False)

#Guardar una lista d titulos
df_dic.to_excel('Diccionario de datos/dic_Titulos.xlsx', header=False, index=False)

