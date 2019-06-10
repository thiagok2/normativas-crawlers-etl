from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'ceero.csv'
conselho = 'ceero'

# Cabeçalho
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])


# Resoluções
url =  'http://www.seduc.ro.gov.br/cee/index.php/2012-08-09-15-26-07.html'   
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
content_atos = soup.find('div', {"id": "maincontent"})
aResolucoes= content_atos.find_all('tr')
i = 1
for tr in aResolucoes:
    tds = tr.findAll('td')

    tagTitulo = tds[0]
    tagEmenta = tds[1]
    tagLink =   tds[2].a

    titulo = tagTitulo.text.strip().split('-')[0]
    sigla = tagTitulo.text.strip().split('-')[1].strip()

    numero = titulo.replace('Res. n.','').strip()
    ano = int(titulo.split('/')[1])

    if ano > 80:
        ano = ano + 1900
    else:
        ano = ano + 2000

    data = str(ano)+'-12-31'
    
    titulo = titulo +' '+sigla
    ementa = tagEmenta.text.strip()

    documento = urljoin(url, str(tagLink.get('href')))
    id = conselho + '-' + tipo + '-' + str(i)
    i = i + 1

    with open(arquivo, 'a', encoding='utf-8' , newline = '') as csvfile:
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])