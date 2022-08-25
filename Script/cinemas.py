import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import date

today = date.today()

# usa el web driver compatible con la version del navegador chrome, si se actualiza se tiene que descargar otro drive
browser = webdriver.Chrome('C:\\chromedriver.exe')

vector = ('''function v(e1){
              var v1=[];
              for (let e of e1.children) {
                  v1.push(e);
              }
              return v1; 
              };
                ''')
# para navegar entre hijos anidados donde "e1" es el elemento padre y "v1" es el vector de navegacion
# retorna el ultimo elemento de navegacion
hijos = ('''function h(e1,v1){
            var c1=e1;
            for (let e of v1) {
                c1=c1.children[e];
            }
            return c1;
            };
            ''')
browser.get('https://cinemas.com.ni/')
time.sleep(1)
id1 = ['cnm_all_date_desktop', 'cnm_local_desktop',
       'cnm_peliculas_desktop', 'cnm_formato_desktop', 'cnm_horarios_desktop']


def s1(i):
    return browser.execute_script(vector+'''
                                  var r1=[];
                                  for (var v1=1;v1<v(document.querySelector("#'''+i+'''")).length;v1++){
                                        r1.push([v(document.querySelector("#'''+i+'''"))[v1].innerText,v(document.querySelector("#'''+i+'''"))[v1].getAttribute('value')]);  
                                    };
                                  return r1;''')


def s2(i, v):
    seleccion1 = Select(browser.find_element(By.ID, i))
    seleccion1.select_by_value(v[1])
    time.sleep(1)


p1 = s1(id1[0])
#print(p1)

matriz=list()
s2(id1[0], p1[0])
for a in s1(id1[1]):
    s2(id1[1], a)
    for b in s1(id1[2]):
        s2(id1[2], b)
        x1=list()
        for c in s1(id1[3]):
            s2(id1[3], c)
            for d in s1(id1[4]):
                x1.append(d[0])
                matriz.append([today.strftime('%d-%m-%Y'),'Nicaragua','Cinemas',a[0],b[0],d[0]])
            
        #matriz.append([a[0],b[0],x1])
        #df[matriz] = matriz.tolist()
#print(matriz)

df = pd.DataFrame(matriz)
print(df)

df.to_excel('cinemas - '+today.strftime('%d-%m-%Y')+'.xlsx')
browser.close()