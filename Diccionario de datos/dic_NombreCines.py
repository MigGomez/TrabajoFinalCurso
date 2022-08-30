import pandas as pd
import numpy as np

df_k = pd.read_excel('Data Collection/Cinemark - 28-08-2022.xlsx')
df_po = pd.read_excel('Data Collection/Cinepolis - 28-08-2022.xlsx')
df_ms = pd.read_excel('Data Collection/Cinemas - 28-08-2022.xlsx')

df_k.loc[df_k.Pais=='Panamá','Pais']='Panama'
df_po.loc[df_po.Pais=='El salvador','Pais']='El Salvador'

df1 = df_k[['Pais','Nombre Cine']].drop_duplicates()
df2 = df_po[['Pais','Nombre Cine']].drop_duplicates()
df3 = df_ms[['Pais','Nombre Cine']].drop_duplicates()

df_dic = pd.concat([df1, df2, df3], axis=0)

df_dic.to_excel("Diccionario de datos/dic_nombreCine.xlsx", index=False)
#print(df_dic)