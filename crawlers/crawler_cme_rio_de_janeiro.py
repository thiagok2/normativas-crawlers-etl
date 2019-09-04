from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'cme_rio_de_janeiro.csv'
conselho = 'cme_rio_de_janeiro'

# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])

# Todos os atos
url =  'http://www.rio.rj.gov.br/web/sme/exibeconteudo?id=1122731'   
page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')

# Pegar os metadados
atos = soup.find('div', class_ = 'bodyContent')
atas = atos.find_all('p')
atos = atos.find_all('a')
atas_anos = {}

for i in range(0,len(atos)):             
    aux = atos[i].text        
    if any(c in aux for c in ('Base', 'Plano Nacional','Conselheiros','Pareceres','Clique')):
        atos[i].unuse = True                 

for i in range(0,len(atas)):
    if 'Clique' in atas[i].text:        
        lim = i+3
        break

for i in range(0,lim):
    atas[i].unuse = True

for ata in atas:
    if (not ata.unuse and 'Ata' not in ata.text):
        ano_atual = ata.text
        ano_atual = ano_atual.replace(' ','')
    elif(not ata.unuse and len(ata.text)>1):
        nome = ata.text.replace(' ','',1)            
        nome = nome.replace(chr(160),'')
        atas_anos[nome] = ano_atual

ileis = 1
idecs = 1
ires = 1
idel = 1
iind = 1
iata = 1
for ato in atos:
    tipo = ''
    numero = ''
    data = ''
    ementa = ''
    documento = ''
    titulo = ''
    assunto = ''
    processo = ''
    relator = ''
    interessado = ''
    if(not ato.unuse):
        content = ato.text
        documento = urljoin(url, str(ato.get('href')))
        
        if 'Lei' in content:
            tipo = 'lei'            
            titulo = content
            if '- ' in content:
                titulo = titulo[:titulo.find(' -')]
                ementa = content[content.find('- ')+2:]            
            numero = titulo[titulo.find('nº ')+3:]
            numero = numero.replace(',','')
            numero = numero[:numero.find(' de')]
            data = titulo[titulo.find('de')+3:]        
            id = conselho + '-' + tipo + '-' + str(ileis)
            ileis += 1                
        
        elif 'Decreto' in content: 
            tipo = 'decreto'            
            titulo = content
            numero = content[content.find('nº ')+3:content.find(',')]                                                
            data = titulo[titulo.find('de')+3:]        
            id = conselho + '-' + tipo + '-' + str(idecs)
            idecs += 1         

        elif 'Resolução' in content: 
            tipo = 'resolucao'
            titulo = content.replace(',','')
            if '(' in titulo:
                ementa = titulo[titulo.find('(')+1:titulo.find(')')]
                titulo = titulo[:titulo.find('(')]
            numero = titulo[titulo.find('n')+3:titulo.find(' de')]
            data = titulo[titulo.find('de')+3:]
            id = conselho + '-' + tipo + '-' + str(ires)
            ires += 1   

        elif 'Deliberação' in content: 
            tipo = 'deliberacao'
            titulo = content.replace('Nº','nº')                                    
            if 'º' in titulo:
                numero = titulo[titulo.find('º')+1:]                                        
                numero = numero.replace(' ','')
            else:
                numero = titulo[titulo.find('ão')+3:]                        
            id = conselho + '-' + tipo + '-' + str(idel)
            idel += 1   
        
        elif 'Indicação' in content:
            tipo = 'indicacao'
            titulo = content            
            numero = titulo[titulo.find('º')+2:]                                                                    
            id = conselho + '-' + tipo + '-' + str(iind)
            iind += 1   

        elif 'Ata' in content: 
            tipo = 'ata'              
            if(content=='Ata 50'):
                content = 'Ata 507'         
            content = content.replace(chr(160),'')
            data = atas_anos[content]
            titulo = content + '/' + data               
            numero = content[content.find(' ')+1:]                
            id = conselho + '-' + tipo + '-' + str(iata)
            iata += 1                                    
        if(titulo!=''):
            with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:            
                #c = csv.writer(csvfile, delimiter=';')
                c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])    

