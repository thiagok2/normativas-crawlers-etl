from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'cme_porto_alegre.csv'
conselho = 'cme_porto_alegre'

# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])

# Resoluções
url =  'https://www2.portoalegre.rs.gov.br/smed/default.php?p_secao=613'   
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
atos = soup.find('div', id = 'conteudo')
atos = atos.find_all('p')

i = 1
for ato in atos:     
    tags_a = ato.find_all('a')
    text = ato.text
    text = text.split('\n')
    for ta in tags_a:
        documento =  urljoin(url, str(ta.get('href')))
        titulo = ta.text
        numero = titulo.replace('Resolução CME/PoA nº ','')
        data = numero[numero.find('/',2)+1:]                           
        for txt in text:
            if ta.text in txt:                
                ementa = txt.replace(ta.text,'')
                ementa = ementa.replace(chr(160),'')                          
                ementa = ementa.replace('-','',1)
                ementa = ementa.lstrip()
        id = conselho + '-' + tipo + '-' + str(i)
        i = i + 1        
           
        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
            #c = csv.writer(csvfile, delimiter=';')
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])

# Indicações
url =  'https://www2.portoalegre.rs.gov.br/smed/default.php?p_secao=614'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
tipo = 'indicacao'
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
atos = soup.find('div', id = 'conteudo')
atos = atos.find_all('p')

i = 1
for ato in atos:     
    tags_a = ato.find_all('a')
    text = ato.text
    text = text.split('\n')
    for ta in tags_a:
        documento =  urljoin(url, str(ta.get('href')))
        titulo = ta.text
        numero = titulo.replace('Indicação CME/PoA nº ','')
        data = numero[numero.find('/',2)+1:]        
        for txt in text:
            if ta.text in txt:                
                ementa = txt.replace(ta.text,'')
                ementa = ementa.replace(chr(160),'')                          
                ementa = ementa.replace('-','',1)
                ementa = ementa.lstrip()
        id = conselho + '-' + tipo + '-' + str(i)
        i = i + 1       
     
        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
            #c = csv.writer(csvfile, delimiter=';')
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])

# Pareceres anteriores a 2019
url =  'https://www2.portoalegre.rs.gov.br/smed/default.php?p_secao=612'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
tipo = 'parecer'
numero = ''
data = ''
processo = ''
relator = ''
interessado = ''
assunto = ''
ementa = ''
documento = ''
titulo = ''

#Pegar as urls
content = soup.find('div', id = 'conteudo')
tas = content.find_all('a')
links = []
for ta in tas:
    if 'Pareceres' in ta.text:
        links.append(ta.get('href'))

links.sort()

i = 1

for link in links:    
    # Pegar os metadados
    page = http.request('GET', link)
    soup = BeautifulSoup(page.data, 'lxml')        
    atos = soup.find('table')
    atos = atos.find('table')
    atos = atos.find_all('tr')

    for ato in atos:           
        if ato.find('a'):                                        
            text = ato.text.replace(ato.find('a').text,'')            
            text_arr = [txt.strip() for txt in text.split('  ')]
            ementa = ""
            for txt in text_arr:
                txt = txt.replace('\n','')
                ementa += txt.replace('\t','')              
            tag_a = ato.find('a')            
            documento =  urljoin(url, str(tag_a.get('href')))
            titulo = tag_a.text.strip()
            text_arr = [txt.strip() for txt in titulo.split('  ')]
            titulo = ""
            for txt in text_arr:
                txt = txt.replace('\n','')
                txt = txt.replace('//','/')
                titulo += txt.replace('\t','')                                                
            numero = titulo[titulo.find('º')+2:]
            data = numero[numero.find('/',2)+1:]                                
            
            id = conselho + '-' + tipo + '-' + str(i)
            i = i + 1

            with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
                #c = csv.writer(csvfile, delimiter=';')
                c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])

# Pareceres 2019
url =  'https://www2.portoalegre.rs.gov.br/smed/default.php?p_secao=612'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
tipo = 'parecer'
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
atos = soup.find('div', id = 'conteudo')
atos = atos.find_all('h3')

for ato in atos:   
    if 'CME' in ato.text:  
        tags_a = ato.find_all('a')
        text = ato.text
        text = text.split('\n')
        for ta in tags_a:
            documento =  urljoin(url, str(ta.get('href')))
            titulo = ta.text
            numero = titulo.replace('Parecer CME/PoA nº ','')
            data = numero[numero.find('/')+1:]                                
            for txt in text:
                if ta.text in txt:                
                    ementa = txt.replace(ta.text,'')
                    ementa = ementa.replace(chr(160),'')                          
                    ementa = ementa.replace('-','',1)
                    ementa = ementa.lstrip()
            id = conselho + '-' + tipo + '-' + str(i)
            i = i + 1

            with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
                #c = csv.writer(csvfile, delimiter=';')
                c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])    