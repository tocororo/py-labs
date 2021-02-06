#!/usr/bin/env python
from DataCollect import collect, getDataInstance
from Database.instanceOfDao import InstanceOfDao
import sys


value = ''
# Q43229
while value != '5':
    value = input(str(""" 
    1 - Crear tablas instanceOf y subClass
    2 - Obtener instancias y subclases de wikidata. 
    3 - Actualizar informacion sobre instancias.
    4 - Crear copia de instancias y actualizar informacion en ella.
    5 - Eliminar tablas
    6 - Salir.
    Elija una opcion del 1-5: """))
    if value == '1':
        InstanceOfDao.createTableInstance()
        InstanceOfDao.createTableSubclass()
    elif value == '2':
        _class = input(str('Provea un id de clase de wikidata: '))
        collect(_class)
    elif value == '3':
        InstanceOfDao.updateFieldsInstancesToNull()
        getDataInstance('original')
    elif value == '4':
        InstanceOfDao.createInstanceCopy()
        InstanceOfDao.updateCopyFieldsInstancesToNull()
        getDataInstance('copy')
    elif value == '4':
        InstanceOfDao.dropTables()
        InstanceOfDao.dropFunctions()
    elif value == '6':
        sys.exit()

if __name__ == '__main__':
    ...