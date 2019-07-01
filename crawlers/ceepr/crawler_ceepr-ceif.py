from bs4 import BeautifulSoup,NavigableString
import urllib3
from urllib.parse import urljoin
import csv
import time


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

arquivo = 'ceepr-par.csv'
conselho = 'ceepr'

#########################################################################################################################
########### Cria documento
# Cabeçalho do csv
with open(arquivo, 'a+', encoding='utf-8', newline = '') as csvfile:
    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])


#############

urls =  [
        ('http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=253', 'CEIF'),
        ('http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=254',  'CEMEP'),
        ('http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=44', 'CES'),
        ('http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=43', 'CEB')
    ]

i = 1
for url, env in urls:

    page = http.request('GET', url)
    soup = BeautifulSoup(page.data, 'html5lib')
    tipo = ''
    numero = ''
    data = ''
    processo = ''
    relator = ''
    interessado = ''
    ementa = ''
    documento = ''
    titulo = ''
   
    divPage = soup.find('div', {"id": "page"})
    assunto = divPage.find('h1').text
    linksAno = divPage.find_all('a')

    
    time.sleep(1)
    for link in linksAno:
        tipo = 'PAR'
        ano = link.text.strip()
        url1 = link.get('href')
        
        time.sleep(0.5)
        if ano and int(ano) != 9999:
            print(ano)
            try:
                page1 = http.request('GET', url1)
                soup1 = BeautifulSoup(page1.data, 'html5lib')
            
                divPageMeses = soup1.find('div', {"id": "page"})
                linksMes = divPageMeses.find_all('a')
            except:
                print(url1)
                print('--------------')
        
            linksMes = (a for a in linksMes if 'Voltar' not in a.text and a.text.strip() and not a.text.strip().endswith('.pdf'))
            time.sleep(0.5)
            for linkMes in linksMes:
                mes = linkMes.text.strip()
                urlMes = linkMes.get('href')
                
                if ano:
                    try:
                        print(ano + ' - ' + mes + ' - ' + urlMes)

                        pageFinal = http.request('GET', urlMes)
                        soupFinal = BeautifulSoup(pageFinal.data, 'html5lib')

                        divAtos = soupFinal.find('div', {"id": "page"})
                        linksAtos = divAtos.find_all('a') 
                        time.sleep(0.5)
                        for aAto in  linksAtos:
                            if aAto.text and aAto.text.strip() not in ['Voltar', 'Anterior', 'Próximo','Voltar CEIF','Voltar CEMEP','Voltar ao CEMEP','Voltar ao CEIF','Próxima']:
                                titulo = aAto.text
                                documento = aAto.get('href')
                                url = urlMes
                                if 'nº.' in titulo.lower():
                                    numero = titulo.lower().split('nº.')[1].strip().split(',')[0]
                                if ',' in titulo:
                                    data = (titulo.lower().split(',')[1].replace('aprovado em','').strip().replace('-',''))
                                elif '-' in titulo:
                                    data = (titulo.lower().split('-')[1].replace('aprovado em','').strip().replace('-',''))
                                
                                if aAto.next_sibling and str(aAto.next_sibling) and str(aAto.next_sibling).strip() and str(aAto.next_sibling).strip() != '-':
                                    ementa = str(aAto.next_sibling)
                                elif aAto.next_sibling and aAto.next_sibling.next_sibling and str(aAto.next_sibling.next_sibling).strip() and str(aAto.next_sibling.next_sibling).strip() != '-' :
                                    ementa = str(aAto.next_sibling.next_sibling)
                                elif aAto.parent and aAto.parent.next_sibling and str(aAto.parent.next_sibling).strip() and str(aAto.parent.next_sibling).strip() != '-' :
                                    ementa = str(aAto.parent.next_sibling)
                                else:
                                    ementa = (titulo)
                                
                                ementa = ementa.strip()
                                if ementa.startswith('- ') or ementa.startswith(', '):
                                    ementa = ementa[2:]

                                print(titulo + ' - ' + ementa)
                                id = conselho + '-' +  env + '-' + tipo + '-' + ano +'-'+ str(i)
                                i = i + 1

                                time.sleep(0.50)
                                with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
                                    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                                    c.writerow([id, url, tipo, numero, data, processo, relator, interessado, ementa, assunto, documento,titulo])
                    except:
                        print('ERRROOO:::'+ano + ' - ' + mes + ' - ' + urlMes)
                

        

#########################################################################################################################
##### 