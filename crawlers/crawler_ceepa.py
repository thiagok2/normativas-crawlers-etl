from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'ceepa.csv'
conselho = 'ceepa'

# Cabeçalho
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])


# Resoluções
url =  'http://www.cee.pa.gov.br/?q=node/108'   
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
i = 1

# Pegar os metadados
content_atos = soup.find('div', {"id": "ContentNode"})
aResolucoes= content_atos.find_all('a')

for a in aResolucoes:
    if a.text.strip():  
        documento = urljoin(url, str(a.get('href')))
        ementa = a.text

        titulo = ementa.split('-')[0]
        ementa = "-".join(ementa.split('-')[1:]).strip()

        numero = titulo.split(" DE ")[0].replace('RESOLUÇÃO','').replace('N','').replace('.','').strip()
        ano = titulo.split(" DE ")[-1].strip()
        data = " de ".join(titulo.split(" DE ")[1:])
        
        numero = (numero + '/' +ano)

        id = conselho + '-' + tipo + '-' + str(i)
        i = i + 1
        
        with open(arquivo, 'a', encoding='utf-8' , newline = '') as csvfile:
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])