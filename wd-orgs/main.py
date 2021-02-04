#!/usr/bin/env python
from DataCollect import collect, getDataInstance
from Database.instanceOfDao import InstanceOfDao
import sys


value = ''
# Q43229
while value != '4':
    value = input(str(""" 
    1 - Obtener instancias y subclases de wikidata. 
    2 - Actualizar informacion sobre instancias.
    3 - Crear copia de instancias y actualizar informacion en ella.
    4 - Salir.
    Elija una opcion del 1-4: """))
    if value == '1':
        _class = input(str('Prevea un id de clase de wikidata: '))
        collect(_class)
    elif value == '2':
        getDataInstance('2')
    elif value == '3':
        InstanceOfDao.createTableInfo()
        getDataInstance('3')
    elif value == '4':
        sys.exit()

if __name__ == '__main__':
    ...

# _class = input(str('Enter one class id: '))
# get_data = ''
# while _class == '':
#     _class = input(str('Enter one class id: '))
# if _class != '':
#     collect(_class)
#     InstanceOfDao.createTableInfo()
#     while get_data != 'y' or get_data != 'n':
#         get_data = input(str('Enter yes(y) for collect info of instances or no(n) for finish: '))
#         if get_data == 'y':
#             getDataInstance(2)
#         elif get_data == 'n':
#             sys.exit()
        
# array = [1, 2, 3, 4, 8]
# array1 = [0,586,5,54,4,56]
# for num in array:
#         if not any( num == n for n in array1):
#             array1.append(num)
#             print(array1)

# array = [1, 2, 3, 4, 8, 9]
# array1 = [0,586,5,54,4,56]
# 
# array.extend(array1)
# print(array)
