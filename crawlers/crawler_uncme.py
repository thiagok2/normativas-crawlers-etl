from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
from unicodedata import normalize

import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'uncme.csv'
esfera = 'municipal'

# Cabeçalho
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Esfera','Municipio','Estado','Nome','Sigla','Url Curta','Gestão'])


# Metadados dos Municípios
url =  'https://www.uncme.org.br/Pagina-Conselhos.php' 
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
municipio = ''
estado = ''
nome = ''
url_curta = ''
gestao = ''
sigla = ''
i = 1

# Pegar os metadados
municipios = soup.find_all('tr', class_ = 'centralizatexto')

for m in municipios:
    dados = m.find_all('td')        

    municipio = dados[1].text
    
    estado = dados[0].text
    
    nome = 'CONSELHO MUNICIPAL DE EDUCAÇÃO DE ' + municipio.upper() + ' - ' + estado

    sigla = 'CME-' + municipio.replace(' ','-').upper() + '-' + estado
    
    url_curta = normalize('NFKD', municipio).encode('ASCII', 'ignore').decode('ASCII').lower()
    url_curta = url_curta.replace('-', '')
    url_curta = url_curta.replace(' ', '') + '-' + estado.lower()
    
    gestao = 'PRESIDENTE: ' + dados[2].text.upper()

    id = 'uncme-' + str(i)
    i = i + 1
    
    with open(arquivo, 'a', encoding='utf-8' , newline = '') as csvfile:
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,esfera,municipio,estado,nome,sigla,url_curta,gestao])