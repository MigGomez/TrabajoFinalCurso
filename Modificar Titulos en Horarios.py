import pandas as pd
import numpy as np
from fuzzywuzzy import process

cine = ['Cinepolis', 'Cinemark', 'Cinemas']

#generamos el dataframe para concatenar los 3 cines
df_fn = pd.DataFrame()

#llamamos el dic de titulos
df_dic = pd.read_excel('Diccionario de datos/dic_Titulos.xlsx')
dic = df_dic[0].unique()

#Pide fecha de los archivos
fecha = input('Ingrese fecha dd-mm-yyyy:')

#modifica archivo por archivo
for c in cine:
    df = pd.read_excel('Data Collection/'+c+' - '+fecha+'.xlsx')

    titulos = df['Titulo'].unique()

    #Busca coincidencia del nombre del titulo
    for i in titulos:
        x = process.extractOne(i, dic)
        if x[1]>70:
            df['Titulo'] = df['Titulo'].replace([i], x[0])

    #concatenamos el dataframe modicado para seguir con el siguient cine
    df_fn = pd.concat([df_fn, df], axis=0)
    #df.to_excel('Data Transformation/'+c+' - '+fecha+'.xlsx', index=False)

#guarda un solo archivo con los 3 cines
df_fn.to_excel('Data Transformation/Horarios/Horarios - '+fecha+'.xlsx', index=False)
