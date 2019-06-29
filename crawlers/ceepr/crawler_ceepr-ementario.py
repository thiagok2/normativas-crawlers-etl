from bs4 import BeautifulSoup,NavigableString
import urllib3
from urllib.parse import urljoin
import csv
import time
import os  


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

arquivo = 'ceepr-ementario.csv'
conselho = 'ceepr'

#########################################################################################################################
########### Cria documento
# Cabeçalho do csv

if not os.path.isfile(arquivo):
    with open(arquivo, 'w', encoding='utf-8', newline = '') as csvfile:
        c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        c.writerow(['Id','Url','Tipo','Numero','Data','Processo','Relator','Interessado','Ementa','Assunto','Documento','Titulo'])


#############

urls =  [
        'http://www.cee.pr.gov.br/modules/conteudo/conteudo.php?conteudo=81' #Ementario
    ]

time.sleep(2)
for url in urls:
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

    i = 1
    time.sleep(2)
    linksAno = (a for a in linksAno if 'Cursos aprovados' not in a.text and a.text.strip())
    for link in linksAno:
        tipo = 'Ementa'
        ano = link.text.strip()
        url1 = link.get('href')
        time.sleep(5)
        if ano and int(ano) < 2011:
            print(ano)
            try:
                page1 = http.request('GET', url1)
                soup1 = BeautifulSoup(page1.data, 'html5lib')
            
                divPageMeses = soup1.find('div', {"id": "page"})
                linksMes = divPageMeses.find_all('a')
            except:
                print(url1)
                print('--------------')
        
            linksMes = (a for a in linksMes if 'Voltar' not in a.text and a.text.strip())
            time.sleep(5)
            for linkMes in linksMes:
                mes = linkMes.text.strip()
                urlMes = linkMes.get('href')

                try:
                    print(ano + ' - ' + mes + ' - ' + urlMes)

                    if urlMes.endswith('.pdf'):
                        documento = urlMes
                        data = mes + '/'+ str(ano)
                        titulo = 'Ementário - ' + data
                        ementa = titulo
                        id = conselho + '-' + tipo + '-' + ano +'-'+ str(i)
                        i = i + 1

                        print('*** ' + str(i) + ' - ' + titulo + ' - ' + data + ' - ' + documento)
                        time.sleep(1.5)
                        with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
                            c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                            c.writerow([id, url, tipo, numero, data, processo, relator, interessado, ementa, assunto, documento,titulo])
                        continue
                    else:
                        pageFinal = http.request('GET', urlMes)
                        soupFinal = BeautifulSoup(pageFinal.data, 'html5lib')

                        divAtos = soupFinal.find('div', {"id": "page"})
                        linksAtos = divAtos.find_all('a') 
                        time.sleep(2)
                        for aAto in  linksAtos:
                            if aAto.text and aAto.text.strip() not in ['Voltar', 'Anterior', 'Próximo','Voltar CEIF','Voltar CEMEP','Voltar ao CEMEP','Voltar ao CEIF','Próxima']:
                                titulo = aAto.text
                                documento = aAto.get('href')
                                url = urlMes
                                data = ano + '/' + mes
                                numero = data
                                if aAto.next_sibling and str(aAto.next_sibling) and str(aAto.next_sibling).strip() and str(aAto.next_sibling).strip() != '-' and str(aAto.next_sibling).strip() != '<br/>':
                                    ementa = str(aAto.next_sibling)
                                elif aAto.next_sibling and aAto.next_sibling.next_sibling and str(aAto.next_sibling.next_sibling).strip() and str(aAto.next_sibling.next_sibling).strip() != '-' and str(aAto.next_sibling.next_sibling).strip() != '<br/>':
                                    ementa = str(aAto.next_sibling.next_sibling)
                                elif aAto.parent and aAto.parent.next_sibling and str(aAto.parent.next_sibling).strip() and str(aAto.parent.next_sibling).strip() != '-' and str(aAto.parent.next_sibling).strip() != '<br/>':
                                    ementa = str(aAto.parent.next_sibling)
                                else:
                                    ementa = (titulo)

                                id = conselho + '-' + tipo + '-' + ano +'-'+ str(i)
                                i = i + 1

                                print('*** ' + str(i) + ' - ' + titulo + ' - ' + data + ' - ' + documento)
                                time.sleep(0.2)
                                with open(arquivo, 'a', encoding='utf-8', newline = '') as csvfile:
                                    c = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                                    c.writerow([id, url, tipo, numero, data, processo, relator, interessado, ementa, assunto, documento,titulo])
                except Exception as e:
                    print('ERRROOO:::'+ano + ' - ' + mes + ' - ' + urlMes)
                    print(e)
                    print('-----------------------------------------------')                      
                

        

#########################################################################################################################
##### 