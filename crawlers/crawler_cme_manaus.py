from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'cme_manaus.csv'
conselho = 'cme_manaus'

# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])

# Leis
url =  'cme.manaus.am.gov.br/legislacao-2/'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
tipo = 'lei'
numero = ''
data = ''
processo = ''
relator = ''
interessado = ''
assunto = ''
ementa = ''
documento = ''
titulo = ''

# Pegar os metadados
atos = soup.find('div', class_ = 'entryPage')
atos = atos.find_all('li')


i = 1
for ato in atos:     
    tag_a = ato.find('a')
    documento =  urljoin(url, str(tag_a.get('href')))
    titulo = tag_a.text
    if('Lei' in titulo):
        numero = titulo.replace('Lei nº ','')
        numero = numero[0:numero.find(' ')]
        ementa = titulo[titulo.find('– ')+2:]
        titulo = titulo[:titulo.find(' –')]
    elif('Decreto' in titulo):
        numero = titulo.replace('Decreto nº ','')
        numero = str(numero[0:numero.find(' ')])
        ementa = titulo[titulo.find('– ')+2:]   
        titulo = titulo[:titulo.find(' –')]
        tipo = 'decreto' 
        i=1
    
    id = conselho + '-' + tipo + '-' + str(i)
    i = i + 1
    
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
        #c = csv.writer(csvfile, delimiter=';')
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])

# Pareceres
url =  'cme.manaus.am.gov.br/atos-normativos/pareceres/'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
tipo = 'parecer'
numero = ''
data = ''
processo = ''
relator = ''
interessado = ''
assunto = ''
ementa = ''
documento = ''
titulo = ''

# Pegar os links para os anos
anos = []
links_anos = soup.find('div', class_ = 'entryPage')
links_anos = links_anos.find_all('a')

for link_ano in links_anos:    
    ano = str(link_ano.get('href'))
    ano = ano.replace(' ','')
    if(ano!="http://cme.manaus.am.gov.br/pareceres-2006"):        
        anos.append(ano)

i_tot = 1
for ano in anos:
    url =  ano
    page = http.request('GET', url)
    soup = BeautifulSoup(page.data, 'lxml')

    # Pegar os metadados
    atos = soup.find('div', class_ = 'entryPage')
    atos = atos.find_all('p')

    links = []
    ementas = []
    
    for ato in atos:
        cont = 0
        if(ato.find('a')):
            links.append(ato.find('a'))
            if(ato.find('br')):
                aux = ato.find('a')
                aux = aux.text
                ato2 = ato.text                
                ato2 = ato2[ato2.find(aux)+len(aux)+1:]
                if(ato2!=""):
                    ementas.append(ato)                                
                cont = 1
        elif(ord(ato.text[0])!=160 and cont==0 ):
            ementas.append(ato)                    

    for i in range(0,len(links)):    
        documento = urljoin(url, str(links[i].get('href')))
        titulo = links[i].text
        ementa = ementas[i].text
        if titulo in ementa:
            ementa = ementa[ementa.find(titulo)+len(titulo)+1:]
        titulo = titulo.replace('-','/')                
        numero = titulo.replace('Parecer nº ','')
        numero = numero.replace('CME/','')
        if(' – ' in numero):            
            titulo = titulo[:titulo.find(' – ')]
            data = numero[numero.find(' – ')+3:]
            numero = numero[:numero.find(' – ')]
        else:
            data = numero[numero.find('/')+1:]    
        id = conselho + '-' + tipo + '-' + str(i_tot)
        i_tot += 1      
    
        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
            #c = csv.writer(csvfile, delimiter=';')
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])    


# Resoluções
url =  'cme.manaus.am.gov.br/atos-normativos/resolucoes/'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
tipo = 'resolucao'
numero = ''
data = ''
processo = ''
relator = ''
interessado = ''
assunto = ''
ementa = ''
documento = ''
titulo = ''

# Pegar os links para os anos
anos = []
links_anos = soup.find('div', class_ = 'entryPage')
links_anos = links_anos.find_all('a')

for link_ano in links_anos:    
    ano = str(link_ano.get('href'))
    ano = ano.replace(' ','')
    anos.append(ano)

i_tot = 1
for ano in anos:
    url =  ano
    page = http.request('GET', url)
    soup = BeautifulSoup(page.data, 'lxml')

    # Pegar os metadados
    atos = soup.find('div', class_ = 'entryPage')
    atos = atos.find_all('p')

    links = []
    ementas = []
    
    for ato in atos:
        cont = 0
        if(ato.find('a')):
            links.append(ato.find('a'))
            if(ato.find('br')):
                aux = ato.find('a')
                aux = aux.text
                ato2 = ato.text                
                ato2 = ato2[ato2.find(aux)+len(aux)+1:]
                if(ato2!="" and ord(ato.text[0])!=160):                    
                    ementas.append(ato)                             
                cont = 1
        elif((ord(ato.text[0])!=160 or len(ato.text)>1) and cont==0 ):            
            ementas.append(ato)            

    for i in range(0,len(links)):    
        documento = urljoin(url, str(links[i].get('href')))
        titulo = links[i].text
        if(titulo[0]==' '):
            titulo = titulo[1:]
        ementa = ementas[i].text
        ementa = ementa.replace('<strong>','')
        ementa = ementa.replace('</strong>','')
        if titulo in ementa:
            ementa = ementa[ementa.find(titulo)+len(titulo)+1:]
        titulo = titulo.replace('-','/')                
        numero = titulo.replace('Resolução nº ','')
        numero = numero.replace('CME/','')
        if("n" in numero):
            numero = numero[-8:]
        if(' – ' in numero):            
            titulo = titulo[:titulo.find(' – ')]
            data = numero[numero.find(' – ')+3:]
            numero = numero[:numero.find(' – ')]
        else:
            data = numero[numero.find('/')+1:]    
        id = conselho + '-' + tipo + '-' + str(i_tot)
        i_tot += 1      
    
        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
            #c = csv.writer(csvfile, delimiter=';')
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])    