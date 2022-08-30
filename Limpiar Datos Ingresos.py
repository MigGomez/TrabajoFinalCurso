import pandas as pd
import numpy as np
from fuzzywuzzy import process
from datetime import date

today = date.today()

#generamos el dataframe para concatenar los paises
df_fn = pd.DataFrame()

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

    df.insert(0, "Pais", c, allow_duplicates=False)

    #h = list(df)
    #for i in h:
       # if "$" in i:
        #    df[i]=df[i].apply('{:.2f}'.format)
         #   df[i]='$'+df[i]
        
    df_fn = pd.concat([df_fn, df], axis=0)

    #df.to_excel('Data Transformation/'+c+'.xlsx', sheet_name=c, index=False)



df_fn.to_excel('Data Transformation/Horarios/Ingresos.xlsx',sheet_name="Ingresos Centro America", index=False)

df_t = pd.DataFrame(titulos)
df_t = df_t.drop_duplicates()
df_titulos = pd.concat([df_titulos, df_t], axis=0)
df_titulos = df_titulos.drop_duplicates()

df_titulos.to_excel('Diccionario de datos/dic_Titulos.xlsx',  index=False)


#Modificamos el archivo ingresos otra vez
df = pd.read_excel('Data Transformation/Horarios/Ingresos.xlsx')
a=int()
ingresos = list()
adm = list()
for i in list(df):
    if "$" in i:
        ingresos.append(i)
        a+=1
    
    if "Adm" in i:
        adm.append(i)
        #print(i)

filas=list()
for nc in df.index:
    
    for fn in range(a):
        l = ingresos[fn], df['Pais'][nc], df['Nombre Cine'][nc], df['Titulo'][nc], df['Ciudad'][nc], df['Cine'][nc], df[ingresos[fn]][nc], df[adm[fn]][nc]
        filas.append(l)
   
     
df_nuevo = pd.DataFrame(filas, columns=['Fecha','Pais','Nombre Cine','Titulo','Ciudad','Cine','Ingresos','Asistencia'])

fech = df_nuevo['Fecha'].unique()
from datetime import datetime

for i in fech:
    c = i+"2022"
    a = datetime.strptime(c,'%a  %d-%b $%Y')
    #print(a.strftime('%d-%m-%Y'))
    df_nuevo['Fecha'].replace([i],[a.strftime('%d-%m-%Y')], inplace=True)

df_nuevo.to_excel('Data Transformation/Horarios/Ingresos.xlsx', sheet_name="Ingresos Centro America", index=False)
