from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin
import csv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()
 
arquivo = 'ceeba.csv'
conselho = 'ceeba'

# Cabeçalho do csv
with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])

# Todos os Atos Normativos
url =  'http://www.conselhodeeducacao.ba.gov.br/modules/conteudo/conteudo.php?conteudo=64'   
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
lista = soup.find(id = 'lista-exercicio')
exercicios = lista.find_all('li')
i=1
for exercicio in exercicios:
    if(exercicio.find('span')):
        data = (exercicio.find('span').text)        
        atos_exercicio = exercicio.find('ul').find_all('li')
        for ato in atos_exercicio:
            if(ato.find('a')):
                link = ato.find('a')
                documento =  urljoin(url, str(link.get('href')))
                titulo = 'Resolução ' + link.text
                ementa = ato.text
                numero = titulo[titulo.find('N')+2:]                
                numero = numero[:numero.find('/')]
                numero = numero.replace(' ','')
                id = conselho + '-' + tipo + '-' + str(i)
                i = i + 1                
        
    id = conselho + '-' + tipo + '-' + str(i)
    with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:            
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow([id,url,tipo,numero,data,processo,relator,interessado,ementa,assunto,documento,titulo])            