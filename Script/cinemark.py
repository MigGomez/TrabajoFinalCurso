import time
from selenium import webdriver
import pandas as pd
from datetime import date

today = date.today()

#usa el web driver compatible con la version del nabegador chrome, si se actualiza se tiene que descargar otro drive
browser = webdriver.Chrome('C:\\chromedriver.exe')
browser.get('https://www.cinemarkca.com/index')
browser.maximize_window()
time.sleep(2)

browser.execute_script(
    'document.querySelector("#modal-theatre-select > div > div.modal-theatre-select-body.modal-theatre-selector-container > div > div > div > button:nth-child(1)").click()')
time.sleep(1)
# para convertir en vector un elemto con multiples hijos donde "e1" es el elemento padre
# retorna el un vector con los elementos hijos
vector = ('function v(e1){' +
          '    var v1=[]; ' +
          '    for (let e of e1.children) {' +
          '        v1.push(e);' +
          '    }' +
          '    return v1; ' +
          '};')
# para navegar entre hijos anidados donde "e1" es el elemento padre y "v1" es el vector de navegacion
# retorna el ultimo elemento de navegacion
hijos = ('function h(e1,v1){' +
         '    var c1=e1;' +
         '    for (let e of v1) {' +
         '        c1=c1.children[e];' +
         '    }' +
         '    return c1; ' +
         '};')

p1 = browser.execute_script(vector+hijos+'var r1=[];' +
                            'v(document.querySelector("#accordion")).forEach(el1 =>{v(h(el1,[0,1,0,0])).forEach(el2=>{r1.push([h(el1,[0,0,0]).innerText,h(el2,[0]).innerText,h(el2,[0]).href]);})});' +
                            'return r1;')
#print(p1)
matriz=list()
for i in p1:
    browser.get(i[2])
    time.sleep(2)
    browser.execute_script(
        'document.querySelector("#header > div.row.header-inner > div > div.col-xs-6.col-sm-6.col-md-6.col-lg-6.menu-header.hidden-responsive > ul > li:nth-child(2) > a").click()')
    time.sleep(2)
    elemento = 'document.querySelector("#movie-show-container > div")'
    p2=browser.execute_script(vector+hijos+'var cnt=["'+i[0]+'","'+i[1]+'"];var titulo="";var r1=[];v(' + elemento +
                           ').forEach(el1=>{v(h(el1,[1])).forEach(el2=>{if(el2.className!="movie-title"){v(h(el2,[1])).forEach(el3=>{if(el3.className!="legal"){r1.push([cnt[0],cnt[1],titulo,el3.innerText])}})}else{titulo=h(el2,[1]).innerText;}})});return r1;'
                           )
    #p3=[today.strftime('%d-%m-%Y'),p2[0][0],'Cinemark',p2[0][1],p2[0][2],p2[0][3]]
    #print(p2)
    #print(p3)
    for l in p2:
        a= today.strftime('%d-%m-%Y'),l[0],'Cinemark',l[1],l[2],l[3]
        matriz.append(a)    

    #matriz+=p2
    
    #matriz1.append([today.strftime('%d-%m-%Y'),p2[0][0],'Cinemark',p2[0][1],p2[0][2],p2[0][3]])
    #print(matriz1)

    
df = pd.DataFrame(matriz,columns=['Fecha','Pais','Cine','Nombre Cine','Titulo','Hora'])
df=df [df.Pais != 'Curacao']
df.loc[df.Pais=='Panamá','Pais']='Panama'

df.to_excel('Cinemark - '+today.strftime('%d-%m-%Y')+'.xlsx', index=False)
browser.close()