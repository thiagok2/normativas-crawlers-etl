from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'cme_fortaleza.csv'
conselho = 'cme_fortaleza'

# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])

# Leis
url =  'http://cme.sme.fortaleza.ce.gov.br/index.php/com-phocadownload-tags/downloads/category/4-leis'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
tipo = 'lei'
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
atos = soup.find('div', class_ = 'pd-category')
atos = atos.find_all('div', class_ = 'pd-filebox')

i = 1
for ato in atos:  
    titulo = ato.find('div', class_ = 'pd-title').text
    tag_a = ato.find('div', class_ = 'pd-float')
    tag_a = tag_a.find('a')            
    documento =  urljoin(url, str(tag_a.get('href')))
    numero = tag_a.text
    data = numero[numero.find('de_')+3:numero.find('ok')].replace('-','/')
    numero = numero[numero.find('_')+1:numero.find('_de')]    
    id = conselho + '-' + tipo + '-' + str(i)
    i = i + 1
       
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
        #c = csv.writer(csvfile, delimiter=';')
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])

# Pareceres
url =  'http://cme.sme.fortaleza.ce.gov.br/index.php/e'   
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
atos = soup.find('div', class_ = 'pd-category')
atos = atos.find_all('div', class_ = 'pd-filebox')

i = 1
for ato in atos:  
    titulo = ato.find('div', class_ = 'pd-title').text
    numero = ''
    if 'º' in titulo:
        numero = titulo[titulo.find('º')+1:]
    elif '°' in titulo:
        numero = titulo[titulo.find('°')+1:]
    numero = numero.strip()
    if ' - ' in numero:
        numero = numero[:numero.find(' - ')]
    data = ''
    if '20' in titulo:
        data = titulo[titulo.find('20'):titulo.find('20')+4]   
    if 'de' in numero:
        data = numero[numero.find(' ')+1:]
        numero = numero[:numero.find(' ')]+'/'+data[-4:]

    tag_a = ato.find('div', class_ = 'pd-float')
    tag_a = tag_a.find('a')                
    documento =  urljoin(url, str(tag_a.get('href')))

    ementa = ato.find('div', class_ = 'pd-button-details').find('a').get('onmouseover')    
    if '<p>' in ementa:
        ementa = ementa[ementa.find('<p>')+3:ementa.find('</p>')]
    else:
        ementa = ''
    
    id = conselho + '-' + tipo + '-' + str(i)
    i = i + 1
    
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
        #c = csv.writer(csvfile, delimiter=';')
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])

# Resoluções
url =  'http://cme.sme.fortaleza.ce.gov.br/index.php/resolucoes'   
data = {'limit': '0'}
page = http.request('POST', url, data)
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
atos = soup.find('div', class_ = 'pd-category')
atos = atos.find_all('div', class_ = 'pd-filebox')

i = 1
for ato in atos:  
    titulo = ato.find('div', class_ = 'pd-title').text
    ementa = titulo[titulo.find('/2')+5:]
    ementa = ementa.strip('- ')
    ementa = ementa.strip()
    titulo = titulo[:titulo.find('/2')+5]    
    
    numero = ''
    if 'º' in titulo:
        numero = titulo[titulo.find('º')+1:]
    elif '°' in titulo:
        numero = titulo[titulo.find('°')+1:]
    else:
        numero = titulo[titulo.find(' ')+1:]
    numero = numero.strip()
    data = ''    
    data = numero[-4:]   

    tag_a = ato.find('div', class_ = 'pd-float')
    tag_a = tag_a.find('a')                
    documento =  urljoin(url, str(tag_a.get('href')))
    
    id = conselho + '-' + tipo + '-' + str(i)
    i = i + 1
    
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
        #c = csv.writer(csvfile, delimiter=';')
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])

# Atas
url =  'http://cme.sme.fortaleza.ce.gov.br/index.php/com-phocadownload-files/atas'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')
tipo = 'ata'
numero = ''
data = ''
processo = ''
relator = ''
interessado = ''
assunto = ''
ementa = ''
documento = ''
titulo = ''

#Pegar as urls externas
content = soup.find('div', class_ = 'pd-category')
tas = content.find_all('div', class_ = 'pd-subcategory')
links = []
for ta in tas:        
    links.append(ta.find('a').get('href'))

links_int = []

#Pegar as urls internas
for link in links:       
    page = http.request('GET', 'http://cme.sme.fortaleza.ce.gov.br'+link)
    soup = BeautifulSoup(page.data, 'lxml')
    content = soup.find('div', class_ = 'pd-category')
    tas = content.find_all('div', class_ = 'pd-subcategory')    
    for ta in tas:        
        links_int.append(ta.find('a').get('href'))    

links_int.append('/index.php/com-phocadownload-tags/downloads/category/29-atas-de-2019')

i = 1
for link in links_int:    
    # Pegar os metadados
    page = http.request('GET', 'http://cme.sme.fortaleza.ce.gov.br'+link)
    soup = BeautifulSoup(page.data, 'lxml')
    atos = soup.find('div', class_ = 'pd-category')
    atos = atos.find_all('div', class_ = 'pd-filebox')
        
    for ato in atos:  
        titulo = ato.find('div', class_ = 'pd-title').text.strip()     

        tag_a = ato.find('div', class_ = 'pd-float')
        tag_a = tag_a.find('a')
        documento =  urljoin(url, str(tag_a.get('href')))

        if 'BICAMERAL' in titulo:
            numero = ''
            data = tag_a.text[tag_a.text.find('1'):tag_a.text.find('.pdf')]
            data = data.replace('.','/')
        else:    
            numero = ''
            if 'da' in titulo:
                numero = titulo[titulo.find('da')+2:].strip()
                numero = numero[:numero.find(' ')]
            elif 'DA' in titulo:
                numero = titulo[titulo.find('DA')+2:].strip()
                numero = numero[:numero.find(' ')]

            data = ''
            if '-' in titulo:
                data = titulo[titulo.find('ria')+3:].strip()
                data = data.strip('-')
                data = data.strip()
                data = data.replace('-','/')
                data = data.replace('.','/')
                if len(data)<10:
                    final = data[-2:]
                    data = data[:-2]
                    data = data + '20' + final
            else:
                data = titulo[-4:]
                if 'LENO' in data:
                    data = '2019'        
        
        id = conselho + '-' + tipo + '-' + str(i)
        i = i + 1

        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
            #c = csv.writer(csvfile, delimiter=';')
            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
            c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])