from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'ceerj.csv'
conselho = 'ceerj'

# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])

# Deliberacoes e Indicacoes
url =  'http://www.cee.rj.gov.br/deliberacoes.asp'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
tipo = ''
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
atos = soup.find(id = 'colunaCentral').find_all('li')
idel = 1
iind = 1
for ato in atos:
    link = ato.find('a')
    titulo = link.text.replace('.pdf','')        
    documento =  urljoin(url, str(link.get('href')))
    t = titulo[0]
    numero = titulo[7:]        
    data = titulo[2:6]
    if(t=='D'):
        tipo = 'deliberacao'        
        titulo = 'Deliberação ' + numero + '/' + data        
        idel = idel + 1        
    elif(t=='I'):
        tipo = 'indicacao'                
        titulo = 'Indicação ' + numero + '/' + data        
        iind = iind + 1

    id = conselho + '-' + tipo + '-' + str(idel)
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:            
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])            

# Pareceres
url =  'http://www.cee.rj.gov.br/pareceres.asp'   
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
atos = soup.find(id = 'colunaCentral').find_all('li')
i = 1
for ato in atos:
    comp = ''
    link = ato.find('a')
    titulo = link.text.replace('.pdf','')            
    documento =  urljoin(url, str(link.get('href')))
    data = titulo[2:6]
    if 'homologados' in titulo:
        titulo = 'Pareceres Homologados ' + data
    else:                 
        if 'normativo' in titulo:
            comp = ' Normativo'
        elif 'CEB' in titulo:
            comp = ' CEB'
        numero = titulo[7:10]   
        titulo = 'Parecer' + comp + ' ' + numero + '/' + data
    id = conselho + '-' + tipo + '-' + str(i)
    i = i + 1
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
        #c = csv.writer(csvfile, delimiter=';')
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])