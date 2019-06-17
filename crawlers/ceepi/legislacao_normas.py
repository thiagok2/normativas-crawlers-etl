from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin, quote
import urllib.parse
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'ceepi-normas.csv'
conselho = 'ceepi'

# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])

# Resoluções
url =  'http://www.ceepi.pro.br/normativos.htm'   
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
uls = soup.find_all('ul')

i = 1
for ul in uls[:2]:
    atos = ul.find_all('li')

    for ato in atos:
        link = ato.find('a')
        if link:
            i = i + 1
            documento =  urljoin(url, str(link.get('href')))
            titulo = link.text.strip()
            if(link.next_sibling):
                ementa = link.next_sibling.string.strip()
            tipo = titulo.split(' ')[0].strip()
            numero = titulo.split(' ')[-1].strip()
            id = conselho + '-' + tipo + '-' + str(i)
            if '/' in numero:
                ano = numero.split('/')[-1]
                
                     
            with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
                c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])