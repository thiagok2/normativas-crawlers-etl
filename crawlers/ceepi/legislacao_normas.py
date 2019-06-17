from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
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
atos = soup.find_all('p', class_ = 'MsoNormal')

i = 1
for ato in atos:
    link = ato.find('a')
    
    
    if link.find('href'):
        documento =  urljoin(url, str(link.get('href')))

    #     print(documento)

    #ementa = link.next_sibling.text
    #titulo = link.text


    # numero = titulo.replace('Resolução ','')
    # ementa = ato.find('div').text.replace('\r','').replace('\n','').replace('\t','').strip()
    # data = titulo.split('/')[1][0:4]
    # id = conselho + '-' + tipo + '-' + str(i)
    # i = i + 1
    # with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
    #     #c = csv.writer(csvfile, delimiter=';')
    #     c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    #     c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])