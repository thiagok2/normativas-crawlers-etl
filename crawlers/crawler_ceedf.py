from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'ceefd-resolucoes-recomendacoes.csv'
conselho = 'ceefd'

# Cabeçalho
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])


# Resoluções
url =  'http://cedf.se.df.gov.br/resolucoes/resolicao-cedf'   
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

# Pegar os metadados
content_atos = soup.find('article', class_ = 'item')
resolucoes = content_atos.find_all('p')

j = 1
for i in range(0,len(resolucoes)):
    links = resolucoes[i-1].find_all('a')
    titulo = resolucoes[i-1].text
    ementa = resolucoes[i].text
    if len(links) != 0:
        documento =  urljoin(url, str(links[0].get('href')))
        data = titulo.split('/')[1][0:4]
        numero = titulo.replace('Resolução n° ','').replace(' - CEDF','').replace(' ','')
        print('documento:')
        print(documento)
        print('ementa')
        print(ementa)
        print('titulo:')
        print(titulo)
        print('\n')
        id = conselho + '-' + tipo + '-' + str(j)
        j = j + 1
        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
            #c = csv.writer(csvfile, delimiter=';')
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])
    i = i + 1
    





# Recomendações
url =  'http://cedf.se.df.gov.br/recomendacoes'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
tipo = 'recomendação'
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
content_atos = soup.find('article', class_ = 'item')
resolucoes = content_atos.find_all('p')

j = 1
for i in range(0,len(resolucoes)):
    links = resolucoes[i-1].find_all('a')
    titulo = resolucoes[i-1].text
    ementa = resolucoes[i].text
    if len(links) != 0:
        data = titulo.split('/')[1][0:4]
        documento =  urljoin(url, str(links[0].get('href')))
        numero = titulo.replace('Recomendação n° ','').replace(' - CEDF','').replace(' ','')
        print('documento:')
        print(documento)
        print('ementa')
        print(ementa)
        print('titulo:')
        print(titulo)
        print('\n')
        id = conselho + '-' + tipo + '-' + str(j)
        j = j + 1
        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
            #c = csv.writer(csvfile, delimiter=';')
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])
    i = i + 1
    