from urllib.parse import urljoin, quote, unquote_plus
from bs4 import BeautifulSoup
import urllib3

url= 'http://www.ceepi.pro.br/Resoluções%20%20%202018/0%20resolução%202018.htm'
#url = 'http://www.ceepi.pro.br/Resoluções%20%20%202001B/0%20resoluções%202001B.htm'

url = url.replace('Resoluções','Resolu%C3%A7%C3%B5es').replace('resolução','resolu%C3%A7%C3%A3o')
print(url)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

page = http.request('GET', url)
soup = BeautifulSoup(page.data, 'lxml')