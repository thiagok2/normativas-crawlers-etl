from bs4 import BeautifulSoup,NavigableString
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

arquivo = 'ceepr-cp.csv'
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
urls =  ['http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=707', #2019
        'http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=641',  #2018
        'http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=573',  #2017
        'http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=517',  #2016
        'http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=458',  #2015
        'http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=374',  #2014
        'http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=302'   #2013
        'http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=275']  #2012

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

    ano = divPage.findChild().text.strip().split(' ')[0]
    print('---------------------------------------------')
    print(ano)
    links = divPage.find_all('a')

    i = 1
    #lista = (x for x in xyz if x not in a)
    links = (a for a in links if 'Voltar' not in a.text and a.text.strip())
    for link in links:
        tipo = 'PAR'
        titulo = link.text.strip()
        documento = link.get('href')
        

        if 'nº.' in titulo.lower():
            numero = titulo.lower().split('nº.')[1].strip().split(',')[0]
        
        if ',' in titulo:
            data = (titulo.lower().split(',')[1].replace('aprovado em','').strip().replace('-',''))
        
        ementa = ''
        
        element = link
        if element.next_sibling and str(element.next_sibling) and str(element.next_sibling).strip() and str(element.next_sibling).strip() != '-':
            ementa = (titulo + ' - ' + str(element.next_sibling))
        elif element.next_sibling and element.next_sibling.next_sibling and str(element.next_sibling.next_sibling).strip() and str(element.next_sibling.next_sibling).strip() != '-' :
             ementa = (titulo + ' - ' + str(element.next_sibling.next_sibling))
        elif element.parent and element.parent.next_sibling and str(element.parent.next_sibling).strip() and str(element.parent.next_sibling).strip() != '-' :
             ementa = (titulo + ' - ' + str(element.parent.next_sibling))
        else:
             ementa = (titulo)
        
        
        
        id = conselho + '-' + tipo + '-' + str(i)
        i = i + 1

        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id, url, tipo, numero, data, processo, relator, interessado, ementa, assunto, documento,titulo])

#########################################################################################################################
##### 