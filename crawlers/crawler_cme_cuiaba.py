from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'cme_cuiaba.csv'
conselho = 'cme_cuiaba'

# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])

# Leis
url =  'https://cmecuiaba.com.br/legislacao/#1533040441347-65b07c56-5122'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
tipo = 'lei'
numero = ''
data = ''
assunto = ''
ementa = ''
documento = ''
titulo = ''
processo = ''
relator = ''
interessado = ''

# Pegar os metadados
atos = soup.find('div', class_ = 'vc_tta-panel-body')
atos = atos.find_all('a')

i = 1
for ato in atos:     
    content = ato.text
    documento = urljoin(url, str(ato.get('href')))
    if 'Lei Nº 5' in content:        
        titulo = content[:content.find('_')]
        ementa = content[content.find('_')+1:]
        titulo = titulo.replace('-','/')
        numero = titulo[titulo.find('Nº ')+3:]
        data = titulo[titulo.find('/')+1:]        
        id = conselho + '-' + tipo + '-' + str(i)
        i = i + 1        
    
        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:            
            #c = csv.writer(csvfile, delimiter=';')
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])

# Resoluções
url =  'https://cmecuiaba.com.br/legislacao/#1533040441388-bf188ae0-74ce'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
tipo = 'resolucao'
numero = ''
data = ''
assunto = ''
ementa = ''
documento = ''
titulo = ''
processo = ''
relator = ''
interessado = ''

# Pegar os metadados
atos = soup.find_all('div', class_ = 'vc_tta-panel-body')
atos = atos[2]
atos = atos.find_all('a')
i = 1
for ato in atos:     
    content = ato.text
    documento = urljoin(url, str(ato.get('href')))        

    if 'CME' in content:        
        if 'RESOLUÇÃO' in content:
            titulo = content[:content.find('CME')+3]
            ementa = content[content.find('DO'):]
            titulo = titulo.replace('-',' ',3)
            titulo = titulo.replace('-','/')
            ementa = ementa.replace('-', ' ')
            numero = titulo[titulo.find('nº ')+3:titulo.find('C')-1]
            data = numero[numero.find('/')+1:]
            id = conselho + '-' + tipo + '-' + str(i)
            i = i + 1
        else:
            titulo = content[:content.find('_')]
            ementa = content[content.find('_')+1:]
            titulo = titulo.replace('-','/')
            numero = titulo[titulo.find('Nº ')+3:titulo.find('/',30)]
            data = numero[numero.find('/')+1:]
            id = conselho + '-' + tipo + '-' + str(i)
            i = i + 1
    
        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
            #c = csv.writer(csvfile, delimiter=';')
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])        