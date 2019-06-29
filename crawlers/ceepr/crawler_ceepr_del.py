from bs4 import BeautifulSoup,NavigableString
import urllib3
from urllib.parse import urljoin
import csv
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

arquivo = 'ceepr-del.csv'
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
urls =  ['http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=93']  #2012

for url in urls:
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
    #lista = (x for x in xyz if x not in a)
    links = (a for a in links if 'Voltar' not in a.text and a.text.strip() and 'celepar7cta' not in a.get('href') )
    for link in links:
        time.sleep(1.0)
        tipo = 'DEL'
        ano = link.text.strip()
        linkAno = link.get('href')
        
        pageAno = http.request('GET', linkAno)
        soupAno = BeautifulSoup(pageAno.data, 'html5lib')

        divPageAno = soupAno.find('div', {"id": "page"})
        linksDels = divPageAno.find_all('a')

        #consultaPublicaPDF
        linksDels = (a for a in linksDels if 'Voltar' not in a.text and 'consultaPublicaPDF' not in a.get('href') and a.get('href') != '#')
        for linkDel in linksDels:
            time.sleep(0.5)
            documento = linkDel.get('href').strip()
            titulo = linkDel.text.strip()
            numero = ''
            if 'nº' in titulo.lower():
                numero = titulo.lower().split('nº')[1]
            if 'n.º' in titulo.lower():
                numero = titulo.lower().split('n.º')[1]

            if ',' in numero:
                numero = numero.split(',')[0]
            elif '-' in numero:
                numero = numero.split('-')[0]
            data = ''
            if ',' in titulo:
                data = titulo.lower().split(',')[1]
            elif '-' in titulo:
                data = titulo.lower().split('-')[1]
            if data:
                data = data.lower().replace('aprovado em','').replace('aprovada em','').replace('aprovados em','').strip().replace('-','')
            #if '-'  in titulo:
            
            id = conselho + '-' + tipo + '-' + str(i)
            i = i + 1

            with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
                c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                c.writerow([id, url, tipo, numero, data, processo, relator, interessado, ementa, assunto, documento,titulo])

#########################################################################################################################
##### 