#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.

from lxml import html
import requests
import os

def get_agent():
    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'}


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

def get_article_download_ojs(dictionary, save_dir):
    timeout = 30
    ext = ''
    dir_open = save_dir + '/'
    os.makedirs(save_dir, exist_ok=True)
    for key in dictionary:
        response = requests.get(dictionary[key], verify = False, timeout = timeout)
        print(response.headers['Content-Type'])
        if(response.text != ''):
            if(response.headers['Content-Type'] == 'application/pdf'):
                ext = '.pdf'
                filename = key + ext
                if(response.headers['Content-Disposition']):
                    content_disposition = response.headers['Content-Disposition']
                    indice_1 = content_disposition.index('"') #obtenemos la posición del primer carácter "
                    indice_2 = content_disposition.rfind('"') #obtenemos la posición del ultimo carácter "
                    filename = content_disposition[indice_1 + 1:indice_2]
                export_file = open(dir_open + filename, 'wb')
                export_file.write(response.content)
                export_file.close()
            if(response.headers['Content-Type'] == 'text/html'):
                ext = '.html'
                filename = key + ext
                if(response.headers['Content-Disposition']):
                    content_disposition = response.headers['Content-Disposition']
                    indice_1 = content_disposition.index('"') #obtenemos la posición del primer carácter "
                    indice_2 = content_disposition.rfind('"') #obtenemos la posición del ultimo carácter "
                    filename = content_disposition[indice_1 + 1:indice_2]
                export_file = open(dir_open + filename, 'wb')
                export_file.write(response.content)
                export_file.close()
    return 'ok'


def get_article_files(url, save_dir):
    res = get_urls_download_ojs(url)
    get_article_download_ojs(res, save_dir)
