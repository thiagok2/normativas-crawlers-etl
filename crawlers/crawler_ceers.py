from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
ini = time.time()
abainicial = 1
abafinal = 2000
i = 1

arquivo = 'ceers-aba-'+str(abainicial)+'-a-aba-'+str(abafinal)+'.csv'
conselho = 'ceers'

# Cabeçalho
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])

# Aba: 1 a 1996
# Fazer requisição em cada aba
for aba in range (abainicial,abafinal + 1):
    url =  'http://www.ceed.rs.gov.br/lista/610/Atos%20do%20Conselho%20Estadual/busca=;*;*;*;T/' + str(aba)  
    page = http.request('GET', url)
    soup = BeautifulSoup(page.data, 'lxml')    
    atosaba = soup.find('ul', class_ = 'cConteudoListaSimples')    

    if atosaba != None:  
        atos = atosaba.find_all('a')
        tipo = ''
        numero = ''
        processo = ''
        relator = ''
        interessado = ''
        assunto = ''
        ementa = ''
        documento = ''
        titulo = ''
        for ato in atos:
            titulo = ato.text
            tipo = ato.text.split(' ')[0]
            numero = ''
            if ' ' in ato.text:
                numero = ato.text.split(' ')[2]
            data = ''
            if '/' in numero:
                data = numero.split('/')[1]
            linkato = urljoin(url, str(ato.get('href')))
            pageato = http.request('GET', linkato)
            soupato = BeautifulSoup(pageato.data, 'lxml')   
            #paragrafosementa = soupato.find_all('p', class_ = 'Ementa')
            ementa = soupato.find('div', class_ = 'cArticleTexto').text.replace('\r',' ').replace('\n',' ').replace('\t',' ').strip()
            #ementa = ''
            #for paragrafoementa in paragrafosementa:
            #    ementa = ementa + paragrafoementa.text + ' '
            anexo = soupato.find('div', class_ = 'cConteudoAnexosItem')
            documento = ''
            if anexo != None:
                anexo = anexo.find('a')
                documento = urljoin(url, str(anexo.get('href')))        
            id = conselho + '-' + tipo + '-' + str(i)
            i = i + 1
            print(id)
            with open(arquivo, 'a', encoding='utf-8' , newline = '') as csvfile:
                c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])
            
            # Monitorando o tempo
            fim = time.time()
            
            segundos = fim-ini
            minutos = segundos / 60
            horas = minutos / 60
            
            if segundos < 60:
                print('Duração: ' + str(segundos) + ' s')
            elif minutos < 60:
                print('Duração: ' + str(minutos) + ' min')
            else:
                print('Duração: ' + str(horas) + ' h')
            print('\n')
