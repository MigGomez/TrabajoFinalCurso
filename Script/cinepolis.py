import time
from selenium import webdriver
from datetime import date
import pandas as pd

today = date.today()

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
    time.sleep(5)
    
    
    elemento1 = 'document.querySelector("#cmbCiudades")'
    elemento2 = 'document.querySelector("#cmbComplejos")'
    elemento3 = 'document.querySelector("#carteleraCiudad > section.col7.listaCarteleraHorario")'
     
    p3=browser.execute_script(vector+'''var r1=[];
                           for (var v1=1;v1<v('''+elemento1+''').length;v1++){
                                   r1.push(v('''+elemento1+''')[v1].getAttribute('clave'));
                            };
                           return r1;
                           ''')
    print(p3)
    
    for i in p3:            
        browser.get(u+'/'+i+'/')
        i = i.replace('-', ' ')
        time.sleep(5)
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
            l[1]=l[1].split(' ')[0].replace('-',' ')
        matriz+=p5
        #print(p5)
        matriz1+=p5
        #matriz1.append([p5[0,0],p5[0,1],p5[0,2]])
        
print(matriz)
data_df = pd.DataFrame(matriz1)
df = pd.DataFrame(matriz)
data_df.to_excel('cinepolis - '+today.strftime('%d-%m-%Y')+'.xlsx', index=False)
df.to_excel('cinepolis1 - '+today.strftime('%d-%m-%Y')+'.xlsx')