from bs4 import BeautifulSoup,NavigableString
import urllib3
from urllib.parse import urljoin
import csv
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

arquivo = 'ceepr-ead.csv'
conselho = 'ceepr'

#########################################################################################################################
########### Cria documento
# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])


#############
# http://www.cee.ms.gov.br/atos-normativos/indicacoes/
# http://www.cee.ms.gov.br/atos-normativos/deliberacoes/
urls =  [
    'http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=36',
    'http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=37'
    ] 

for url in urls:
    time.sleep(1.0)
    page = http.request('GET', url)
    soup = BeautifulSoup(page.data, 'html5lib')
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

    divPage = soup.find('div', {"id": "page"})

    links = divPage.find_all('a')

    i = 1
    links = (link for link in links if link.get('href') != '#')

    for link in links:
        time.sleep(0.5)
        titulo = link.text.strip()
        documento = link.get('href')
        
        numero = ''
        if 'nº' in titulo.lower():
            numero = titulo.lower().split('nº')[1].strip()
            
        tipo = titulo.split(' ')[0] 
        ementa = ''
        
        element = link
        if element.next_sibling and str(element.next_sibling) and str(element.next_sibling).strip() and str(element.next_sibling).strip() != '-':
            ementa = str(element.next_sibling)
        else:
            ementa = (titulo)
            
        ementa = ementa.strip()
        if ementa.startswith(': '):
            ementa = ementa[2:]

        id = conselho + '- ead - '+ tipo + '-' + str(i)
        i = i + 1

        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id, url, tipo, numero, data, processo, relator, interessado, ementa, assunto, documento,titulo])

#########################################################################################################################
##### 