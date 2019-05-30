from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

arquivo = 'ceese.csv'
conselho = 'ceese'

#########################################################################################################################
########### Cria documento
# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])


#############
url =  'http://www.cee.se.gov.br/resolucoes_normativas.asp'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'html5lib')
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

atos = soup.find_all('ul', class_ = 'lista_legislacao')

i = 1
for ato in atos:
    lis = ato.find_all('li')
    titulo = lis[0].text.strip()
    ementa = lis[1].text.strip()
    if(ementa[0] == '-'):
        ementa = ementa[1:].strip()
    tipo = 'resolucao'
    link = lis[0].find('a')
    documento =  urljoin(url, str(link.get('href'))).strip()
    id = conselho + '-' + tipo + '-' + str(i)
    i = i + 1

    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id, url, tipo, numero, data, processo, relator, interessado, ementa, assunto, documento,titulo])

#########################################################################################################################
##### portaria

url =  'http://www.cee.se.gov.br/portaria.asp'
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'html5lib')
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

portarias = soup.find('ul', class_ = 'links_list')
atos = portarias.find_all('li')

for li in atos:
    link = li.find('a')
    documento =  urljoin(url, str(link.get('href'))).strip()
    titulo = link.text.strip()
    id = conselho + '-' + tipo + '-' + str(i)
    i = i + 1
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id, url, tipo, numero, data, processo, relator, interessado, ementa, assunto, documento,titulo])

###########################################################
### legislacao
url =  'http://www.cee.se.gov.br/legislacao.asp'
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'html5lib')
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

legislacao = soup.find_all(['h3','h2'], class_ = 'list_title')

for leg in legislacao:
    leg_titulo = leg.text 
    collect_li =leg.findNext('ul').find_all('li')
    for li in collect_li:
        link = li.find('a')
        documento =  urljoin(url, str(link.get('href'))).strip()
        titulo = leg_titulo + ' - ' +link.text.strip()
        id = conselho + '-' + tipo + '-' + str(i)
        i = i + 1
        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id, url, tipo, numero, data, processo, relator, interessado, ementa, assunto, documento,titulo])