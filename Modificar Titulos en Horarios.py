import pandas as pd
import numpy as np
from fuzzywuzzy import process

cine = ['Cinepolis', 'Cinemark', 'Cinemas']

df_fn = pd.DataFrame()
df_dic = pd.read_excel('Diccionario de datos/dic_Titulos.xlsx')
dic = df_dic[0].unique()

fecha = input('Ingrese fecha dd-mm-yyyy:')

for c in cine:
    df = pd.read_excel('Data Collection/'+c+' - '+fecha+'.xlsx')

    titulos = df['Titulo'].unique()

    for i in titulos:
        x = process.extractOne(i, dic)
        if x[1]>70:
            df['Titulo'] = df['Titulo'].replace([i], x[0])

    df_fn = pd.concat([df_fn, df], axis=0)
    #df.to_excel('Data Transformation/'+c+' - '+fecha+'.xlsx', index=False)

df_fn.to_excel('Data Transformation/Horarios/Horarios - '+fecha+'.xlsx', index=False)
