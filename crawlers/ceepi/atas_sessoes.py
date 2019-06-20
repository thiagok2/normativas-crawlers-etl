from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin, quote
import urllib.parse
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'ceepi-sessoes_atas.csv'
conselho = 'ceepi'

# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])

# Resoluções
url =  'http://www.ceepi.pro.br/Sess%C3%B5es/sess%C3%B5es.htm'   
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
trs = trs[2:]

i = 1
count = 0
for row in trs:
    columns = row.find_all('td')
    col = 0
    tipos = ['ano', 'Pauta','Ata']
    for td in columns:
        if(col == 0):
            ano = int(td.text)
        else:
            tipo = tipos[col]
            
            links = td.find_all('a')
            for a in links:
                url0 = a.get('href')
                url0 = urljoin(url, str(url0))
                #print('{} - {} - {}'.format(ano, tipo, url0))
                if 'Sessões' in url0:
                    url0 = url0.replace('Sessões','Sess%C3%B5es')
                try:
                    page = http.request('GET', url0)
                    soup = BeautifulSoup(page.data, 'lxml')
                except Exception as e:
                    #url0 = quote(url0)
                    print(str(e))
                    print('url = {}'.format(url0))
                    continue

                table = soup.find('table')
                if table:
                    trs = table.find_all('tr')
                    trs = trs[3:]

                    for _row in trs:
                        cols = _row.find_all('td')
                        _col = 0
                        _mes = ''
                        _url = ''
                        _data = ''
                        _ementa = ''

                        for _td in cols:
                            if(_col == 0):
                                _mes = _td.text.strip()
                            else:
                                links = _td.find_all('a')
                                if(not links):
                                    continue
                                for a in links:
                                    _titulo = tipo + ' - ' + a.text + '/'+ _mes +'/'+ str(ano)
                                    _numero = a.text + '/'+ _mes
                                    _data = a.text + '/'+ _mes + '/' + str(ano)
                                    _documento = urljoin(url0, a.get('href'))
                                    _ementa = _titulo
                                   
                                    count = count + 1
                                    id = conselho + '-'+tipo.lower() +'-'+str(count)
                                    
                                    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
                                        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                                        c.writerow([id,url0,tipo,_numero,_data,processo,relator,interessado,_ementa,assunto,_documento, _titulo])
                            
                            _col = _col + 1
        col = col + 1

print(count)