from lxml import etree, ElementInclude, html
import requests
import os
import urllib.parse
from random import randint

def get_agent():
    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'}

###########################
#      REVISTAS OJS       #
###########################


def get_urls_download_ojs(url):
    '''
    @params
    url: url del articulo a recolectar
    @return:
    retorna un diccionario con las url de descarga de los ficheros asociados al articulo. 
    '''
    sess = requests.Session()
    sess.headers.update(get_agent())
    sess.verify = False
    timeout = 30
    cont = 0
    dictionary = {}
    response = sess.get(url, timeout = timeout)
    doc1 = html.fromstring(response.text)
    element = doc1.xpath('.//a')
    for e in element:
        if(e.get('href')):
            if(url in str(e.get('href'))):
                url_download = str(e.get('href')).replace("view","download")
                dictionary['download'+str(cont)] = url_download
                cont = cont+1        
    return dictionary

def get_article_download_ojs(dictionary, dir, id):
    timeout = 30
    dir_create = dir + id
    dir_open = dir_create + '/'
    os.makedirs(dir_create, exist_ok=True)
    for key in dictionary:
        response = requests.get(dictionary[key], verify = False, timeout = timeout)
        print(response.headers['Content-Type'])
        if(response.text != ''):
            if(response.headers['Content-Type'] == 'application/pdf'):
                filename = key
                if(response.headers['Content-Disposition']):
                    content_disposition = response.headers['Content-Disposition']
                    indice_1 = content_disposition.index('"') #obtenemos la posición del primer carácter "
                    indice_2 = content_disposition.rfind('"') #obtenemos la posición del ultimo carácter "
                    filename = content_disposition[indice_1 + 1:indice_2]
                export_file = open(dir_open + filename, 'wb')
                export_file.write(response.content)
                export_file.close()      
            if(response.headers['Content-Type'] == 'text/html'):
                filename = key
                if(response.headers['Content-Disposition']):
                    content_disposition = response.headers['Content-Disposition']
                    indice_1 = content_disposition.index('"') #obtenemos la posición del primer carácter "
                    indice_2 = content_disposition.rfind('"') #obtenemos la posición del ultimo carácter "
                    filename = content_disposition[indice_1 + 1:indice_2]
                export_file = open(dir_open + filename, 'wb')
                export_file.write(response.content)
                export_file.close() 
    return 'ok'



###########################
#         DSPACE          #
###########################

def get_urls_download_dspace(url):

    sess = requests.Session()
    sess.headers.update(get_agent())
    sess.verify = False
    timeout = 30
    cont = 0
    dictionary = {}
    response = sess.get(url, timeout = timeout)
    doc1 = html.fromstring(response.text)
    element = doc1.xpath('//div[@class="panel panel-info"]//a')
    parsed_url = urllib.parse.urlparse(url)
    url_download = ''
    url_mod = url.replace("handle","bitstream")
    url_dom = parsed_url.scheme +'://'+parsed_url.netloc
    for e in element:
        if(e.get('href')):
            url_href = url_dom + e.get('href')
            if(url_mod in str(url_href) and url_download != url_href):
                url_download = url_href
                dictionary['download'+str(cont)] = url_download
                cont = cont+1        
    return dictionary

def get_article_download_dspace(dictionary, dir, id):
    timeout = 30
    dir_create = dir + id
    dir_open = dir_create + '/'
    cont = 1
    os.makedirs(dir_create, exist_ok=True)
    for key in dictionary:
        response = requests.get(dictionary[key], verify = False, timeout = timeout)
        print('-------------',response.headers['Content-Type'])
        print(response.headers['Content-Disposition'])
        allowed = ['application/pdf', 'text/html']
        if(response.text != ''):
            # if(response.headers['Content-Type'] in allowed):
            filename = id + '_' + str(cont)
            export_file = open(dir_open + filename, 'wb')
            export_file.write(response.content)
            export_file.close()
        cont = cont+1
    return 'ok'






url_ojs = 'https://mendive.upr.edu.cu/index.php/MendiveUPR/article/view/2513'
id = '2513'
direccion =  'data/'
res = get_urls_download_ojs(url_ojs)
get_article_download_ojs(res, direccion, id)

url_dspace = 'https://rc.upr.edu.cu/handle/DICT/3494'
id_d = '1720'
res2 = get_urls_download_dspace(url_dspace)
get_article_download_dspace(res2, direccion, id_d)

#article_diccionario_ojs = get_urls_download_ojs(url)
#article_diccionario_dspace = get_urls_download_dspace(url)
#article_ojs = get_article_download_ojs(get_urls_download_ojs(url),direccion,id)
#article_dspace = get_article_download_dspace(get_urls_download_dspace(url),direccion,id)
#print(article_diccionario_dspace)
#print(article_dspace)