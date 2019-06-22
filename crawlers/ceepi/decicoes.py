from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin, quote
import urllib.parse
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'ceepi-decicoes.csv'
conselho = 'ceepi'

# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])

# Resoluções
url_base_raw =  'http://www.ceepi.pro.br/decisões.htm'
url =  'http://www.ceepi.pro.br/decis%C3%B5es.htm'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
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

center = soup.find('center')
table = center.table

trs = table.find_all('tr')
trs = trs[1:]

i = 1
count = 0
for row in trs:
    columns = row.find_all('td')
    col = 0
    tipos = ['ano', 'parecer','resolucao', 'portaria']
    for td in columns:
        if(col == 0):
            ano = int(td.text)
        else:
            tipo = tipos[col]
            
            links = td.find_all('a')
            for a in links:
                url0 = a.get('href')
                url0 = urljoin(url, str(url0))

                url_raw = urljoin(url_base_raw, str(url0))
                #print('{} - {} - {}'.format(ano, tipo, url0))
              
                url0 = url0.replace('ç','%C3%A7').replace('º','%C2%BA').replace('õ','%C3%B5').replace('ã','%C3%A3')
                try:
                    page = http.request('GET', url0)
                    soup = BeautifulSoup(page.data, 'lxml')
                except Exception as e:
                    #url0 = quote(url0)
                    print(str(e))
                    print('url = {}'.format(url0))
                    continue

                center = soup.find('center')
                if center and center.table:
                    table = center.table

                    trs = table.find_all('tr')
                    trs = trs[1:]

                    for _row in trs:
                        cols = _row.find_all('td')
                        c = 0
                        _numero = ''
                        _url = ''
                        _data = ''
                        _ementa = ''

                        for _td in cols:
                            if(c == 0):
                                _numero = _td.text.strip()[:20]
                                if(_td.a and _numero):
                                    _documento =  urljoin(url_raw, _td.a.get('href'))
                                else:
                                    continue
                            if(c == 1 and _td.text):
                                _data = _td.text.strip()
                                if(not _data):
                                    continue
                            if(c == 2 and _td.text):
                                _ementa = _td.text.strip()
                            
                            c = c + 1

                        if(_data and _numero):
                            count = count + 1
                            _titulo = tipo + ' ' + _numero
                            id = conselho + '_n_'+_numero.replace(' ', '')[0:15]

                            with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
                                c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                                c.writerow([id,url0,tipo,_numero,_data,processo,relator,interessado,_ementa,assunto,_documento, _titulo])
        col = col + 1

print(count)