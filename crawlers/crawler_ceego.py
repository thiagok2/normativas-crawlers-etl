from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

arquivo = 'ceego.csv'
conselho = 'ceego'

#########################################################################################################################
########### Cria documento
# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])


#############
# http://www.cee.ms.gov.br/atos-normativos/indicacoes/
# http://www.cee.ms.gov.br/atos-normativos/deliberacoes/
urls =  ['https://cee.go.gov.br/category/resolucoes/', 'https://cee.go.gov.br/category/resolucoes/page/2/']

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

    #divAtos = soup.find_all('div', class_='info-resolucao')
    articles = soup.find_all('article')
    i = 1
    for article in articles:
        
        href = article.a.get('href')
        url_extrator = urljoin(url, str(href))
        #print(url_extrator)

        div = article.find('div', class_='info-resolucao')
        data = div.p.text
        ementa = div.h4.text

        page_ato = http.request('GET', url_extrator)
        soup_ato = BeautifulSoup(page_ato.data, 'html5lib')

        article_detail = soup_ato.find('article', class_='single-post')

        ementa = article_detail.header.text.strip()

        ementa = ementa  + '\n' +(article_detail.div.text.strip())

        links = article_detail.find_all('a')

        for l in links:
            
            documento = l.get('href')
            titulo = l.text.strip()

            if "clique" in titulo.lower() or not titulo:
                titulo = article_detail.header.text.strip()

            if "parecer" in titulo.lower():
                tipo = 'PAR'
            else:
                tipo = 'RES'

            if 'nº' in titulo.lower():
                numero = titulo.lower().split('nº')[1].strip().split(' ')[0]
            elif 'n°' in titulo.lower():
                numero = titulo.lower().split('n°')[1].strip().split(' ')[0]
            else:
                numero = 'SN'
            
            print(numero + ' - ' + titulo)
            id = conselho + '-' + tipo + '-' + str(i)
            i = i + 1

            with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
                c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                c.writerow([id, url, tipo, numero, data, processo, relator, interessado, ementa, assunto, documento,titulo])

#########################################################################################################################
##### 