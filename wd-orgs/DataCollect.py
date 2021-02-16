from logger_base import logger
from Class.subClass import SubClass
from Class.instanceOf import InstanceOf
from Database.subClassDao import SubClassDao
from Database.instanceOfDao import InstanceOfDao
from Database.SPARQL import get_resultsSubClass, get_resultsInstanceOf, get_infoInstace, get_description_alias

import time
from random import randint

# Q43229
def collect(QID):
    sleep_time = randint(3, 9)
    print('sleep {0} seconds'.format(sleep_time))
    time.sleep(sleep_time)
    sparqlInstanceOf = get_resultsInstanceOf(QID)

    # print(sparqlInstanceOf)
    if sparqlInstanceOf and len(sparqlInstanceOf["results"]["bindings"]) > 0:
        for sparqlI in sparqlInstanceOf["results"]["bindings"]:
            if "countryLabel" in sparqlI and sparqlI["countryLabel"]["value"] == "Cuba":
                instanceCollect(sparqlI)

    postgresSubClass = SubClassDao.select()

    sleep_time = randint(3, 9)
    print('sleep {0} seconds'.format(sleep_time))
    time.sleep(sleep_time)
    sparqlSubClass = get_resultsSubClass(QID)

    if sparqlSubClass and len(sparqlSubClass["results"]["bindings"]) > 0:
        for sparqlS in sparqlSubClass["results"]["bindings"]:
            _QID = sparqlS["item"]["value"].split('/')
            if not any(_QID[len(_QID) - 1] == postgres.getQID() for postgres in postgresSubClass):
                subclass = SubClass(_QID[len(_QID) - 1], sparqlS["itemLabel"]["value"])
                subclass_inserted = SubClassDao.insert(subclass)
                logger.debug(f'Subclass inserted: {subclass_inserted}')
                collect(_QID[len(_QID) - 1])
            else:
                logger.info(f'SubClass exist: {sparqlS["itemLabel"]["value"]}')


def instanceCollect(sparql):
    postgresInstanceOf = InstanceOfDao.select()
    _QID = sparql["item"]["value"].split('/')
    if not any(_QID[len(_QID) - 1] == postgres.getQID() for postgres in postgresInstanceOf):
        instance = InstanceOf(_QID[len(_QID) - 1], sparql["itemLabel"]["value"])
        instance_inserted = InstanceOfDao.insert(instance)
        logger.debug(f'Subclass inserted: {instance_inserted}')
    else:
        logger.info(f'InstanceOf exist: {sparql["itemLabel"]["value"]}')


def getDataInstance(updateType):
    postgresInstanceOf = InstanceOfDao.select()
    for postgres in postgresInstanceOf:
        if postgres.getItemLabel() != 'null' and postgres.getItemLabel() != 'None' and postgres.getItemLabel() != '':
            sleep_time = randint(3, 9)
            print('sleep {0} seconds'.format(sleep_time))
            time.sleep(sleep_time)
            infoInstances = get_infoInstace(postgres.getItemLabel())
            desc_alias = get_description_alias(postgres.getItemLabel())    
                    
            if len(desc_alias["results"]["bindings"]) > 0:
                desc_alias = desc_alias["results"]["bindings"]
                desc_alias = desc_alias[0]   
                if "itemDescription" in desc_alias:                
                    __description = desc_alias["itemDescription"]["value"]
                else:
                    __description = None
                    
                if "itemAltLabel" in desc_alias:                
                    __alias = desc_alias["itemAltLabel"]["value"]
                else:
                    __alias = None
                    
            if len(infoInstances["results"]["bindings"]) > 0:
                    instance = InstanceOf(
                        postgres.getQID(), None, __description, __alias, infoInstances["results"]["bindings"]
                    )
                    if updateType == 'original':
                        instance_updated = InstanceOfDao.update(instance)
                        logger.info(f'Instance Updated: {instance_updated}')
                    elif updateType == 'copy':
                        instance_updated = InstanceOfDao.updateCopy(instance)
                        logger.info(f'Instance Updated: {instance_updated}')
                        