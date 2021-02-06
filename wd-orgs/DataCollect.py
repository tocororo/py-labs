from logger_base import logger
from Class.subClass import SubClass
from Class.instanceOf import InstanceOf
from Database.subClassDao import SubClassDao
from Database.instanceOfDao import InstanceOfDao
from Database.SPARQL import get_resultsSubClass, get_resultsInstanceOf, get_infoInstace


# Q43229
def collect(QID):
    sparqlInstanceOf = get_resultsInstanceOf(QID)
    # print(sparqlInstanceOf)
    if len(sparqlInstanceOf["results"]["bindings"]) > 0:
        for sparqlI in sparqlInstanceOf["results"]["bindings"]:
            if "countryLabel" in sparqlI and sparqlI["countryLabel"]["value"] == "Cuba":
                instanceCollect(sparqlI, QID)

    postgresSubClass = SubClassDao.select()
    sparqlSubClass = get_resultsSubClass(QID)
    if len(sparqlSubClass["results"]["bindings"]) > 0:
        for sparqlS in sparqlSubClass["results"]["bindings"]:
            _QID = sparqlS["item"]["value"].split('/')
            if not any(_QID[len(_QID) - 1] == postgres.getQID() for postgres in postgresSubClass):
                subclass = SubClass(_QID[len(_QID) - 1], sparqlS["itemLabel"]["value"])
                subclass_inserted = SubClassDao.insert(subclass)
                logger.debug(f'Subclass inserted: {subclass_inserted}')
                collect(_QID[len(_QID) - 1])
            else:
                logger.info(f'SubClass exist: {sparqlS["itemLabel"]["value"]}')


def instanceCollect(sparql, subclass):
    postgresInstanceOf = InstanceOfDao.select()
    _QID = sparql["item"]["value"].split('/')
    if not any(_QID[len(_QID) - 1] == postgres.getQID() for postgres in postgresInstanceOf):
        instance = InstanceOf(_QID[len(_QID) - 1], sparql["itemLabel"]["value"], subclass)
        instance_inserted = InstanceOfDao.insert(instance)
        logger.debug(f'Subclass inserted: {instance_inserted}')
    else:
        logger.info(f'InstanceOf exist: {sparql["itemLabel"]["value"]}')


def getDataInstance(updateType):
    _itemDescription = ''
    _instanceOfLabel = ''
    _image = ''
    _inception = ''
    _nativeLabel = ''
    _foundedBy = ''
    _foundedByLabel = ''
    _country = ''
    _countryLabel = ''
    _state = ''
    _stateLabel = ''
    _region = ''
    _regionLabel = ''
    _headquartersLocation = ''
    _numEmployees = ''
    _officialWebSite = ''
    _officialWebSiteLabel = ''
    _ISNI = ''
    _GRID = ''
    _quoraTopic = ''
    _twitterUsername = ''

    postgresInstanceOf = InstanceOfDao.select()
    for postgres in postgresInstanceOf:
        if postgres.getItemLabel() != 'null' and postgres.getItemLabel() != 'None' and postgres.getItemLabel() != '':
            infoInstances = get_infoInstace(postgres.getItemLabel().lower())
            if len(infoInstances["results"]["bindings"]) > 0:
                for info in infoInstances["results"]["bindings"]:
                    QID = info["item"]["value"].split('/')
                    _QID = QID[len(QID) - 1]
                    if "itemDescription" in info:
                        itemDescription = info["itemDescription"]["value"].split('/')
                        _itemDescription = itemDescription[len(itemDescription) - 1]
                    else:
                        _itemDescription = None
                    if "instanceOf" in info:
                        instanceOf = info["instanceOf"]["value"].split('/')
                        _instanceOf = instanceOf[len(instanceOf) - 1]
                    else:
                        _instanceOf = None
                    if "instanceOfLabel" in info:
                        instanceOfLabel = info["instanceOfLabel"]["value"].split('/')
                        _instanceOfLabel = instanceOfLabel[len(instanceOfLabel) - 1]
                    else:
                        _instanceOfLabel = None
                    if "image" in info:
                        image = info["image"]["value"].split('/')
                        _image = image[len(image) - 1]
                    else:
                        _image = None
                    if "inception" in info:
                        inception = info["inception"]["value"].split('/')
                        _inception = inception[len(inception) - 1]
                    else:
                        _inception = None
                    if "nativeLabel" in info:
                        nativeLabel = info["nativeLabel"]["value"].split('/')
                        _nativeLabel = nativeLabel[len(nativeLabel) - 1]
                    else:
                        _nativeLabel = None
                    if "foundedBy" in info:
                        foundedBy = info["foundedBy"]["value"].split('/')
                        _foundedBy = foundedBy[len(foundedBy) - 1]
                    else:
                        _foundedBy = None
                    if "foundedByLabel" in info:
                        foundedByLabel = info["foundedByLabel"]["value"].split('/')
                        _foundedByLabel = foundedByLabel[len(foundedByLabel) - 1]
                    else:
                        _foundedByLabel = None
                    if "country" in info:
                        country = info["country"]["value"].split('/')
                        _country = country[len(country) - 1]
                    else:
                        _country = None
                    if "countryLabel" in info:
                        countryLabel = info["countryLabel"]["value"].split('/')
                        _countryLabel = countryLabel[len(countryLabel) - 1]
                    else:
                        _countryLabel = None
                    if "state" in info:
                        state = info["state"]["value"].split('/')
                        _state = state[len(state) - 1]
                    else:
                        _state = None
                    if "stateLabel" in info:
                        stateLabel = info["stateLabel"]["value"].split('/')
                        _stateLabel = stateLabel[len(stateLabel) - 1]
                    else:
                        _stateLabel = None
                    if "region" in info:
                        region = info["region"]["value"].split('/')
                        _region = region[len(region) - 1]
                    else:
                        _region = None
                    if "regionLabel" in info:
                        regionLabel = info["regionLabel"]["value"].split('/')
                        _regionLabel = regionLabel[len(regionLabel) - 1]
                    else:
                        _regionLabel = None
                    if "headquartersLocation" in info:
                        headquartersLocation = info["headquartersLocation"]["value"].split('/')
                        _headquartersLocation = headquartersLocation[len(headquartersLocation) - 1]
                    else:
                        _headquartersLocation = None
                    if "numEmployees" in info:
                        numEmployees = info["numEmployees"]["value"].split('/')
                        _numEmployees = numEmployees[len(numEmployees) - 1]
                    else:
                        _numEmployees = None
                    if "officialWebSite" in info:
                        officialWebSite = info["officialWebSite"]["value"].split('/')
                        _officialWebSite = officialWebSite[len(officialWebSite) - 1]
                    else:
                        _officialWebSite = None
                    if "officialWebSiteLabel" in info:
                        officialWebSiteLabel = info["officialWebSiteLabel"]["value"].split('/')
                        _officialWebSiteLabel = officialWebSiteLabel[len(officialWebSiteLabel) - 1]
                    else:
                        _officialWebSiteLabel = None
                    if "ISNI" in info:
                        ISNI = info["ISNI"]["value"].split('/')
                        _ISNI = ISNI[len(ISNI) - 1]
                    else:
                        _ISNI = None
                    if "GRID" in info:
                        GRID = info["GRID"]["value"].split('/')
                        _GRID = GRID[len(GRID) - 1]
                    else:
                        _GRID = None
                    if "quoraTopic" in info:
                        quoraTopic = info["quoraTopic"]["value"].split('/')
                        _quoraTopic = quoraTopic[len(quoraTopic) - 1]
                    else:
                        _quoraTopic = None
                    if "twitterUsername" in info:
                        twitterUsername = info["twitterUsername"]["value"].split('/')
                        _twitterUsername = twitterUsername[len(twitterUsername) - 1]
                    else:
                        _twitterUsername = None

                    instance = InstanceOf(
                        _QID, None, _instanceOf,
                        _itemDescription, _instanceOfLabel, _image, _inception, _nativeLabel, _foundedBy, _foundedByLabel,
                        _country, _countryLabel, _state, _stateLabel, _region, _regionLabel, _headquartersLocation,
                        _numEmployees, _officialWebSite, _officialWebSiteLabel, _ISNI, _GRID, _quoraTopic,
                        _twitterUsername
                    )
                    if updateType == 'original':
                        instance_updated = InstanceOfDao.update(instance)
                        logger.info(f'Instance Updated: {instance_updated}')
                    elif updateType == 'copy':
                        instance_updated = InstanceOfDao.updateCopy(instance)
                        logger.info(f'Instance Updated: {instance_updated}')