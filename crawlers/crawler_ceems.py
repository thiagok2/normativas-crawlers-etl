from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

arquivo = 'ceems.csv'
conselho = 'ceems'

#########################################################################################################################
########### Cria documento
# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])


#############
# http://www.cee.ms.gov.br/atos-normativos/indicacoes/
# http://www.cee.ms.gov.br/atos-normativos/deliberacoes/
urls =  ['http://www.cee.ms.gov.br/atos-normativos/pareceres/', 'http://www.cee.ms.gov.br/atos-normativos/indicacoes/', 
        'http://www.cee.ms.gov.br/atos-normativos/deliberacoes/']

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

    divAtos = soup.find('div', class_ = 'entry')

    pAtos = divAtos.find_all('p')
    i = 1
    for p in pAtos:
        if p.descendants:

            try:
                ementa = p.contents[1].strip()
            except:
                if p.contents[0].name is None:
                    continue
                else:
                    ementa = ''
                    #gen = (x for x in xyz if x not in a)
                    listOk = (s for s in p.contents[2:] if s.string is not None)
                    for s in listOk:
                        ementa += s.string + ' '
            if ementa.startswith('– '):
                ementa = ementa[1:]
            #print(ementa)
            if p.a is not None and p.a.text is not None:
                titulo = p.a.text
                if titulo.lower().__contains__('parecer'):
                    tipo = 'parecer'
                elif titulo.lower().__contains__('indicação'):
                    tipo = 'indicacao'
                elif titulo.upper().__contains__('DELIBERAÇÃO'):
                    tipo = 'deliberação'
                else:
                    tipo = 'NA'

                documento = urljoin(url, str(p.a.get('href')))
                
                if titulo.lower().__contains__('n.º') and len(titulo.lower().split('n.º')) >= 2:
                    numero = titulo.lower().split('n.º')[1].strip()
                elif titulo.lower().__contains__('nº') and len(titulo.lower().split('nº')) >= 2:
                    numero = titulo.lower().split('nº')[1].strip()
                elif titulo.lower().__contains__('n°') and len(titulo.lower().split('n°')) >= 2:
                    numero = titulo.lower().split('n°')[1].strip()
                elif titulo.lower().__contains__('n.°') and len(titulo.lower().split('n.°')) >= 2:
                    numero = titulo.lower().split('n.°')[1].strip()
                else:
                    numero = 'NA'
            else:
                continue
            if numero != 'NA' and numero.__contains__('/'):
                ano = numero.split('/')[1] 
            if(len(ano) == 2):
                ano = '19'+ano

            data = ano+'-01-01'

            id = conselho + '-' + tipo + '-' + str(i)
            i = i + 1

            with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
                c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                c.writerow([id, url, tipo, numero, data, processo, relator, interessado, ementa, assunto, documento,titulo])

#########################################################################################################################
##### 