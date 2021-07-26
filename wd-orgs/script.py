#!/usr/bin/env python
import sys

from Controllers.dataCollect import collect, getDataInstance
from Controllers.entities import Entities

value = ''
# Q43229
while value != '6':
    value = input(str(""" 
    1 - Crear tablas instanceOf y subClass
    2 - Obtener instancias y subclases de wikidata. 
    3 - Actualizar informacion sobre instancias.
    4 - Crear copia de instancias y actualizar informacion en ella.
    5 - Eliminar tablas
    6 - Generar JSON instanceOf
    7 - Salir.
    Elija una opcion del 1-7: """))
    if value == '1':
        Entities.createTableInstance()
        Entities.createTableOrganizations()
    elif value == '2':
        _class = input(str('Provea un id de clase de wikidata: '))
        collect(_class)
    elif value == '3':
        getDataInstance('original')
    elif value == '4':
        Entities.createEntitiesCopy()
        getDataInstance('copy')
    elif value == '5':
        Entities.dropTables()
        Entities.dropFunctions()
    elif value == '6':
        Entities.generateJSON()
    elif value == '7':
        sys.exit()

if __name__ == '__main__':
    ...
