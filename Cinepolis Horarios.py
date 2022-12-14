import re
import time
from datetime import datetime
from xmlrpc.client import DateTime
from selenium import webdriver
from datetime import date
import pandas as pd

today = date.today()
ub=['El salvador','Guatemala','Honduras','Panama','Costa Rica']
count=0

# usa el web driver compatible con la version del nabegador chrome, si se actualiza se tiene que descargar otro drive
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


urls = ['https://cinepolis.com.sv/cartelera',
        'https://cinepolis.com.gt/cartelera',
        'https://cinepolis.com.hn/cartelera',
        'https://www.cinepolis.com.pa/cartelera',
        'https://www.cinepolis.co.cr/cartelera']



matriz=list()
matriz1=list()
for u in urls:
    browser.get(u)
    time.sleep(2)
    
    
    elemento1 = 'document.querySelector("#cmbCiudades")'
    elemento2 = 'document.querySelector("#cmbComplejos")'
    elemento3 = 'document.querySelector("#carteleraCiudad > section.col7.listaCarteleraHorario")'
     
    p3=browser.execute_script(vector+'''var r1=[];
                           for (var v1=1;v1<v('''+elemento1+''').length;v1++){
                                   r1.push(v('''+elemento1+''')[v1].getAttribute('clave'));
                            };
                           return r1;
                           ''')
    #print(p3)
    
    for i in p3:            
        browser.get(u+'/'+i+'/')
        i = i.replace('-', ' ')
        time.sleep(2)
        p6=vector+hijos+'''var r1=[];
                                       for (var v0=4;v0<v('''+elemento3+''').length;v0++){
                                            var s1=v('''+elemento3+''')[v0];
                                            for (var v1=1;v1<v(h(s1,[0])).length;v1++){
                                                var s2=v(h(s1,[0]))[v1];
                                                var r2=[];
                                                for (var v2=2;v2<v(h(s2,[1])).length;v2++){
                                                    var s3=v(h(s2,[1]))[v2];
                                                    v(h(s3,[0,1])).forEach(f1=>{
                                                        r2.push(h(f1,[0]).innerText);
                                                    });
                                                };
                                                r1.push(["'''+i+'''",s1.className,h(s2,[1,0,0,0]).innerText,r2]);
                                            };
                                        };
                                       return r1;'''
        p5 = browser.execute_script(vector+hijos+'''var r1=[];
                                       for (var v0=4;v0<v('''+elemento3+''').length;v0++){
                                            var s1=v('''+elemento3+''')[v0];
                                            for (var v1=1;v1<v(h(s1,[0])).length-1;v1++){
                                                var s2=v(h(s1,[0]))[v1];
                                                var r2=[];
                                                for (var v2=2;v2<v(h(s2,[1])).length;v2++){
                                                    var s3=v(h(s2,[1]))[v2];
                                                    v(h(s3,[0,1])).forEach(f1=>{
                                                        r2.push(h(f1,[0]).innerText);
                                                    });
                                                };
                                                r1.push(["'''+i+'''",s1.className,h(s2,[1,0,0,0]).innerText,r2]);
                                            };
                                        };
                                       return r1;''')
        
        for l in p5:

            #print(l)
            l[1]=l[1].strip().split(' ')[0].replace('cinepolis',' ').replace('vip','').replace('-',' ')
            l[1]=l[1].strip()

           
            for h in l[3]:
             
                if (count == 3):         
                    hora=datetime.strptime(h, '%I:%M %p')
                    hora=hora.strftime('%H:%M')
                    
                else:
                    hora=h
                
                a=today.strftime('%d-%m-%Y'),ub[count],'Cinepolis',l[1],l[2],hora
                #print(a)
                matriz.append(a)
       
    count+=1 
            
        
#print(matriz)
data_df = pd.DataFrame(matriz,columns=['Fecha','Pais','Cine','Nombre Cine','Titulo','Hora'])
#df = pd.DataFrame(matriz)

#Corrige el nombre del pais para que coincida con los otros cines
data_df.loc[data_df.Pais=='El salvador','Pais']='El Salvador'

data_df.to_excel('Data Collection/Cinepolis - '+today.strftime('%d-%m-%Y')+'.xlsx', index=False)
#df.to_excel('cinepolis1 - '+today.strftime('%d-%m-%Y')+'.xlsx')
browser.close()
