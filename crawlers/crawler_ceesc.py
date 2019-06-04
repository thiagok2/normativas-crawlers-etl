from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

arquivo = 'ceesc.csv'
conselho = 'ceesc'

#########################################################################################################################
########### Cria documento
# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])


#############
# resoluções
urls =  ['http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-superior/educacao-superior-resolucoes/resolucoes-2',
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-superior/educacao-superior-resolucoes/resolucoes-2?limit=20&limitstart=20',
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-superior/educacao-superior-resolucoes/resolucoes-2?limit=20&limitstart=40',
            
            
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-a-distancia/educacao-a-distancia-resolucoes/resolucoes',
            
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-profissional/educacao-profissional-resolucoes/resolucoes-3',
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-profissional/educacao-profissional-resolucoes/resolucoes-3?limit=20&limitstart=20',
            
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-basica/ensino-infantil/educacao-basica-ensino-infantil-resolucoes/resolucoes-10',
            
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-basica/ensino-medio/educacao-basica-ensino-medio-resolucoes/resolucoes-14',
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-basica/ensino-medio/educacao-basica-ensino-medio-resolucoes/resolucoes-14?limit=20&limitstart=20',
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-basica/ensino-medio/educacao-basica-ensino-medio-resolucoes/resolucoes-14?limit=20&limitstart=40',
            
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-basica/jovens-e-adultos/educacao-basica-jovens-e-adultos-resolucoes/resolucoes-11',
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-basica/jovens-e-adultos/educacao-basica-jovens-e-adultos-resolucoes/resolucoes-11?limit=20&limitstart=20',
            
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-basica/outras-modalidades-de-ensino/educacao-basica/educacao-basica-ensino-especial-resolucoes/resolucoes-13',
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-basica/outras-modalidades-de-ensino/educacao-basica/educacao-basica-ensino-especial-resolucoes/resolucoes-13?limit=20&limitstart=20',

# pareceres
   'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-superior/educacao-superior-parecer/pareceres-2',
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-a-distancia/educacao-a-distancia-parecer/pareceres',
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-profissional/educacao-profissional-parecer/pareceres-3',
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-basica/ensino-infantil/educacao-basica-ensino-infantil-parecer/pareceres-9',
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-basica/ensino-medio/educacao-basica-ensino-medio-parecer/pareceres-13',
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-basica/jovens-e-adultos/educacao-basica-jovens-e-adultos-pareceres/pareceres-10',
            'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-basica/outras-modalidades-de-ensino/educacao-basica/educacao-basica-ensino-especial-parecer/pareceres-12',

# outros
        'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-superior/educacao-superior-outros-atos-normativos/cursos-sequenciais-de-formacao-especifica',
        'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-superior/educacao-superior-outros-atos-normativos/edital-seres',
        'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-superior/educacao-superior-outros-atos-normativos/educacao-especial-1',
        'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-superior/educacao-superior-outros-atos-normativos/nota-tecnica-parfor',
        'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-superior/educacao-superior-outros-atos-normativos/pro-labore',
        'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-superior/educacao-superior-outros-atos-normativos/pos-graduacao',
        'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-superior/educacao-superior-outros-atos-normativos/revalidacao-de-diplomas-estrangeiros',
        'http://www.cee.sc.gov.br/index.php/legislacao-downloads/educacao-superior/educacao-superior-pro-labore'
]

urlBase = 'http://www.cee.sc.gov.br/'
i = 1
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

    divDocs = soup.find_all('div', class_ = 'docman_document')
    urlArray = url.split('/')
    assunto = urlArray[5] + ';' + urlArray[6]

    if(url.__contains__('resolucoes')):
        tipo = 'resolucao'
    if(url.__contains__('pareceres')):
        tipo = 'parecer'
    else:
        tipo = 'NA'
    for div in divDocs:

        a = div.find('a', class_='koowa_header__title_link docman_track_download')
        if(a is None):
            continue
        documento = urljoin(urlBase, str(a.get('href')))
        titulo = a.text.strip()

        if(titulo.__contains__('/')):
            numero = titulo.split(' ')[1].replace('/CEE/SC','')
            ano = numero.split('/')[0]
            data = ano+'-12-31'
        else:
            numero, ano, data = ['','','']

        ementa = div.find('div', class_='docman_description').find('div', itemprop="description").text.strip()
        titulo2 = titulo.lower()
        if tipo == 'NA':
            if titulo2.__contains__('parecer'):
                tipo = 'parecer'
            elif titulo2.__contains__('nota tecnica'):
                tipo = 'nota tecnica'
            elif titulo2.__contains__('resolução'):
                tipo = 'resolução'
            elif titulo2.__contains__('lei complementar'):
                tipo = 'lei complementar'
            
        id = conselho + '-' + tipo + '-' + str(i)
        i = i + 1
        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id, url, tipo, numero, data, processo, relator, interessado, ementa, assunto, documento,titulo])

#########################################################################################################################