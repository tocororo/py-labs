import requests
from random import randint
import json

dominio = 'http://apiassets.upr.edu.cu/'

def get_agent():
    return {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'}

def request_apiassets(url):
    sess = requests.Session()
    
    sess.headers.update(get_agent())

    response = sess.get(url)
    
    return response


def get_all_people():
    itemsPerPage = 1
    page = 1
    people_all = {}
    url = dominio + 'empleados_gras?_format=json&page=' + str(page) + '&itemsPerPage=' + str(itemsPerPage)
    response = request_apiassets(url)
    people = json.loads(response.text)

    while(people['hydra:nextPage']):
        people_all[people['hydra:member'][0]['noCi']] = get_info_people(people['hydra:member'][0]['idExpediente'])
        print(people['hydra:member'][0]['noCi'])
        print(page)
        page = page + 1
        url_new = dominio + 'empleados_gras?_format=json&page=' + str(page) + '&itemsPerPage=' + str(itemsPerPage)
        response = request_apiassets(url_new)
        people = json.loads(response.text)

    return people_all


def get_info_people(id):

    url = dominio + 'empleados_gras/' + str(id)

    people = {}

    response = request_apiassets(url)

    people = json.loads(response.text)

    people['idCategoria'] = get_category(people['idCategoria'])
    people['idCargo'] = get_cargo(people['idCargo'])
    people['idCategoriaDi'] = get_categoryDi(people['idCategoriaDi'])
    people['idGradoCientifico'] = get_gradocientifico(people['idGradoCientifico'])
    people['idMunicipio'] = get_municipios(people['idMunicipio'])
    people['idNivelEscolaridad'] = get_nivel_escolaridad(people['idNivelEscolaridad'])
    people['idProfesion'] = get_profesion(people['idProfesion'])
    people['idProvincia'] = get_provincias(people['idProvincia'])

    return people


def get_category(id):

    url = dominio + 'rh_categorias_ocupacionales/' + str(id)

    category = id

    response = request_apiassets(url)
    
    if(response.status_code == 200):
        json_object = json.loads(response.text)
        category = json_object['descCategoria']

    return str(category)


def get_cargo(id):

    url = dominio + 'rh_cargos/' + str(id)

    cargo = id

    response = request_apiassets(url)
    
    if(response.status_code == 200):
        json_object = json.loads(response.text)
        cargo = json_object['descCargo']

    return str(cargo)
    

def get_categoryDi(id):

    url = dominio + 'rh_categorias_docente_invests/' + str(id)

    categoryDi = id

    response = request_apiassets(url)

    if(response.status_code == 200):
        json_object = json.loads(response.text)
        categoryDi = json_object['descCategoriaDi']
    
    return str(categoryDi)


def get_gradocientifico(id):

    url = dominio + 'rh_grados_cientificos/' + str(id)

    gradocientifico = id

    response = request_apiassets(url)
    
    if(response.status_code == 200):
        json_object = json.loads(response.text)
        gradocientifico = json_object['descGradoCientifico']

    return str(gradocientifico)


def get_municipios(id):

    url = dominio + 'rh_municipios/' + str(id)

    municipio = id

    response = request_apiassets(url)

    if(response.status_code == 200):
        json_object = json.loads(response.text)
        municipio = json_object['descMunicipio']

    return str(municipio)


def get_provincias(id):

    url = dominio + 'rh_provincias/' + str(id)

    provincia = id

    response = request_apiassets(url)

    if(response.status_code == 200):
        json_object = json.loads(response.text)
        provincia = json_object['descProvincia']

    return str(provincia)


def get_nivel_escolaridad(id):

    url = dominio + 'rh_niveles_escolaridads/' + str(id)

    nivel_escolaridad = id

    response = request_apiassets(url)
    
    if(response.status_code == 200):
        json_object = json.loads(response.text)
        nivel_escolaridad = json_object['descNivelEscolaridad']

    return str(nivel_escolaridad)


def get_profesion(id):

    url = dominio + 'rh_profesiones/' + str(id)

    profesiones = id

    response = request_apiassets(url)

    if(response.status_code == 200):
        json_object = json.loads(response.text)
        profesiones = json_object['descProfesion']

    return str(profesiones)
