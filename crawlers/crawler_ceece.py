from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'ceece.csv'
conselho = 'ceece'

# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])

# Resoluções
url =  'https://www.cee.ce.gov.br/download/resolucoes/'   
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

# Pegar os metadados
atos = soup.find_all('li', class_ = 'listfiles__item')

i = 1
for ato in atos:
    link = ato.find('a')
    documento =  urljoin(url, str(link.get('href')))
    titulo = ato.find('em').text
    numero = titulo.replace('Resolução ','')
    ementa = ato.find('div').text.replace('\r','').replace('\n','').replace('\t','').strip()
    data = titulo.split('/')[1][0:4]
    id = conselho + '-' + tipo + '-' + str(i)
    i = i + 1
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
        #c = csv.writer(csvfile, delimiter=';')
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])
        
        
        
        
# Leis
url =  'https://www.cee.ce.gov.br/download/leis/'   
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
atos = soup.find_all('li', class_ = 'listfiles__item')

i = 1
for ato in atos:
    link = ato.find('a')
    documento =  urljoin(url, str(link.get('href')))
    titulo = ato.find('em').text
    numero = titulo.replace('Lei nº ','').replace('lei-','').replace('-estgio-supervisionado','').replace('-','/')
    ementa = ato.find('div').text.replace('\r','').replace('\n','').replace('\t','').strip()
    if '/' in numero:
        data = numero.split('/')[1][0:4]
    else:
        data = ''
    id = conselho + '-' + tipo + '-' + str(i)
    i = i + 1
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
        #c = csv.writer(csvfile, delimiter=';')
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])
        
        
        
        
        
# Publicações
url =  'https://www.cee.ce.gov.br/download/publicacoes/'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
tipo = 'publicacao'
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
atos = soup.find_all('li', class_ = 'listfiles__item')

i = 1
for ato in atos:
    link = ato.find('a')
    documento =  urljoin(url, str(link.get('href')))
    titulo = ato.find('em').text
    #numero = titulo.replace('Lei nº ','').replace('lei-','').replace('-estgio-supervisionado','').replace('-','/')
    ementa = ato.find('div').text.replace('\r','').replace('\n','').replace('\t','').strip()
    if '/' in numero:
        data = numero.split('/')[1][0:4]
    else:
        data = ''
    id = conselho + '-' + tipo + '-' + str(i)
    i = i + 1
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
        #c = csv.writer(csvfile, delimiter=';')
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])
        
        
        
        

# Pareceres anteriores a 2000
url =  'https://www.cee.ce.gov.br/download/anteriores-a-2000/'   
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

# Pegar os metadados
links = soup.find_all('a', class_ = 'listfiles__link')
i = 1
for link in links:
    if len(link.get('href')) > 0:
        documento = urljoin(url, str(link.get('href')))
        ementa = link.find('div').text.replace('\r','').replace('\n','').replace('\t','').strip()
        titulo = link.get('title')
        numero = titulo.replace('Parecer ','')
        if '/' in numero:
            data = numero.split('/')[1][0:4]
        else:
            data = ''
        print('documento:')
        print(documento)
        print('\n')
        id = conselho + '-' + tipo + '-antigos-' + str(i)
        i = i + 1
        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
            #c = csv.writer(csvfile, delimiter=';')
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])
            
            
            
            
# Pareceres após 2000
for ano in range (2000,2020):
    url =  'https://www.cee.ce.gov.br/download/pareceres-' + str(ano) + '/'
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
    
    # Pegar os metadados
    links = soup.find_all('a', class_ = 'listfiles__link')
    i = 1
    for link in links:
        if len(link.get('href')) > 0 and link.get('href') != '#':
            documento = urljoin(url, str(link.get('href')))
            ementa = link.find('div').text.replace('\r','').replace('\n','').replace('\t','').strip()
            titulo = link.get('title')
            numero = titulo.replace('Parecer ','')
            if '/' in numero:
                data = numero.split('/')[1][0:4]
            else:
                data = ''
            print('documento:')
            print(documento)
            print('\n')
            id = conselho + '-' + tipo + '-' + str(ano) + '-' + str(i)
            i = i + 1
            with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
                #c = csv.writer(csvfile, delimiter=';')
                c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])
				