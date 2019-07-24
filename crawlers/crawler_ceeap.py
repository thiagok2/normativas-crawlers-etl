from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'ceeap.csv'
conselho = 'ceeap'

# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])

# Resoluções
with open('pages/resolucoes.html', 'r') as f:
    data = f.read()
url = 'https://cee.portal.ap.gov.br/atos/arquivo/recomendacoes'
soup = BeautifulSoup(data, 'lxml')
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

# Pegar os metadados
tabela = soup.find(id = 'tabela')
tbody = tabela.find('tbody')
atos = tbody.find_all('tr')
i=1
for ato in atos:    
    txt = ato.find('td').text        
    ementa = txt[txt.find('- ')+2:]
    titulo = txt[:txt.find(' -')]
    titulo = titulo.replace('-','/')    
    numero = titulo[titulo.find('º')+2:]    
    data = titulo[-4:]
    documento =  ato.find('a').get('href')
    id = conselho + '-' + tipo + '-' + str(i)
    i = i+1
    if(data.find('/')):
        fatia = data[-2:]         
        fatia_int = int(fatia)
        if(fatia_int<20):
            data = '20'+data[-2:]
        else:    
            data = '19'+fatia               
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:            
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])            

# Demais Resoluções
for j in range(2,6):
    with open('pages/resolucoes'+str(j)+'.html', 'r') as f:
        data = f.read()
    url = 'https://cee.portal.ap.gov.br/atos/arquivo/resolucoes'
    soup = BeautifulSoup(data, 'lxml')
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

    # Pegar os metadados
    tabela = soup.find(id = 'tabela')
    tbody = tabela.find('tbody')
    atos = tbody.find_all('tr')
    for ato in atos:            
        txt = ato.find('td').text        
        txt = txt.replace('-','/',1)
        ementa = txt[txt.find('-')+1:]                        
        if(ementa[0]==' '):
            ementa = ementa[1:]
        if(len(txt)>25):
            titulo = txt[:txt.find('-')]
        else:
            titulo = txt        
        if(titulo[len(titulo)-1]==' '):
            titulo = titulo[:-1]
        numero = titulo[titulo.find('º')+2:]    
        data = titulo[-4:]
        if(ato.find('a')):
            documento =  ato.find('a').get('href')
            if(documento[len(documento)-1]=='/'):
                documento = ''
        else:
            documento = ''
        id = conselho + '-' + tipo + '-' + str(i)
        i = i+1                    
        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:            
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])     

# Portarias
with open('pages/portarias.html', 'r') as f:
    data = f.read()
url = 'https://cee.portal.ap.gov.br/atos/arquivo/portarias'
soup = BeautifulSoup(data, 'lxml')
tipo = 'portaria'
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
tabela = soup.find(id = 'tabela')
tbody = tabela.find('tbody')
atos = tbody.find_all('tr')
i=1
for ato in atos:    
    titulo = ato.find('td').text                
    titulo = titulo.replace('.','/')    
    numero = titulo[titulo.find(' ')+1:]    
    data = titulo[-4:]
    documento =  ato.find('a').get('href')
    id = conselho + '-' + tipo + '-' + str(i)
    i = i+1            
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:            
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])   

# Editais
with open('pages/editais.html', 'r') as f:
    data = f.read()
url = 'https://cee.portal.ap.gov.br/atos/arquivo/editais'
soup = BeautifulSoup(data, 'lxml')
tipo = 'edital'
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
tabela = soup.find(id = 'tabela')
tbody = tabela.find('tbody')
atos = tbody.find_all('tr')
i=1
for ato in atos:    
    titulo = ato.find('td').text                
    titulo = titulo.replace('.','/')        
    if(titulo[len(titulo)-1]==' '):
        titulo = titulo[:-1]
    numero = titulo[titulo.find(' ')+1:]    
    numero = numero.replace(' ','')    
    data = numero[-4:]
    documento =  ato.find('a').get('href')
    id = conselho + '-' + tipo + '-' + str(i)
    i = i+1            
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:            
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo]) 

# Leis
with open('pages/leis.html', 'r') as f:
    data = f.read()
url = 'https://cee.portal.ap.gov.br/atos/arquivo/leis'
soup = BeautifulSoup(data, 'lxml')
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
tabela = soup.find(id = 'tabela')
tbody = tabela.find('tbody')
atos = tbody.find_all('tr')
i=1
for ato in atos:    
    txt = ato.find('td').text        
    ementa = txt[txt.find('- ')+2:]
    titulo = txt[:txt.find(' -')]
    titulo = titulo.replace('-','/')    
    numero = titulo[titulo.find('º')+2:]    
    data = titulo[-4:]
    documento =  ato.find('a').get('href')
    id = conselho + '-' + tipo + '-' + str(i)
    i = i+1
    if(data.find('/')):
        fatia = data[-2:]         
        fatia_int = int(fatia)
        if(fatia_int<20):
            data = '20'+data[-2:]
        else:    
            data = '19'+fatia             
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:            
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])           