from logger_base import logger


class InstanceOf:
    def __init__(self, QID=None, label=None, instanceOf=None, description=None, instanceOfLabel=None, image=None,
                 inception=None, nativeLabel=None, foundedBy=None,
                 foundedByLabel=None, country=None, countryLabel=None, state=None, stateLabel=None, region=None,
                 regionLabel=None, headquartersLocation=None,
                 numEmployees=None, officialWebsite=None, officialWebsiteLabel=None, ISNI=None,
                 GRID=None, quoraTopicID=None, twitterUsername=None):

        self.__QID = QID
        self.__label = label
        self.__instanceOf = instanceOf
        self.__description = description
        self.__instanceOfLabel = instanceOfLabel
        self.__image = image
        self.__inception = inception
        self.__nativeLabel = nativeLabel
        self.__foundedBy = foundedBy
        self.__foundedByLabel = foundedByLabel
        self.__country = country
        self.__countryLabel = countryLabel
        self.__state = state
        self.__stateLabel = stateLabel
        self.__region = region
        self.__regionLabel = regionLabel
        self.__headquartersLocation = headquartersLocation
        self.__numEmployees = numEmployees
        self.__officialWebsite = officialWebsite
        self.__officialWebsiteLabel = officialWebsiteLabel
        self.__ISNI = ISNI
        self.__GRID = GRID
        self.__quoraTopicID = quoraTopicID
        self.__twitterUsername = twitterUsername

    def __str__(self):
        return (
            f'QID: {self.__QID}, '
            f'label: {self.__label}, '
            f'instanceOf: {self.__instanceOf}'
        )

    def getQID(self):
        return self.__QID

    def setQID(self, QID):
        self.__QID = QID

    def getItemLabel(self):
        return self.__label

    def setItemLabel(self, label):
        self.__label = label

    def getInstanceOf(self):
        return self.__instanceOf

    def setInstanceOf(self, instanceOf):
        self.__instanceOf = instanceOf

    def getDescription(self):
        return self.__description

    def setDescription(self, description):
        self.__description = description

    def getInstanceOfLabel(self):
        return self.__instanceOfLabel

    def setInstanceOfLabel(self, instanceOfLabel):
        self.__instanceOfLabel = instanceOfLabel

    def getImage(self):
        return self.__image

    def setImage(self, image):
        self.__image = image

    def getInception(self):
        return self.__inception

    def setInception(self, inception):
        self.__inception = inception

    def getNativeLabel(self):
        return self.__nativeLabel

    def setNativeLabel(self, nativeLabel):
        self.__nativeLabel = nativeLabel

    def getFoundedBy(self):
        return self.__foundedBy

    def setFoundedBy(self, foundedBy):
        self.__foundedBy = foundedBy

    def getFoundedByLabel(self):
        return self.__foundedByLabel

    def setFoundedByLabel(self, foundedByLabel):
        self.__foundedByLabel = foundedByLabel

    def getCountry(self):
        return self.__country

    def setCountry(self, country):
        self.__country = country

    def getCountryLabel(self):
        return self.__countryLabel

    def setCountryLabel(self, countryLabel):
        self.__countryLabel = countryLabel

    def getState(self):
        return self.__state

    def setState(self, state):
        self.__state = state

    def getStateLabel(self):
        return self.__stateLabel

    def setStateLabel(self, stateLabel):
        self.__stateLabel = stateLabel

    def getRegion(self):
        return self.__region

    def setRegion(self, region):
        self.__region = region

    def getRegionLabel(self):
        return self.__regionLabel

    def setRegionLabel(self, regionLabel):
        self.__regionLabel = regionLabel

    def getHeadquartersLocation(self):
        return self.__headquartersLocation

    def setHeadquartersLocation(self, headquartersLocation):
        self.__headquartersLocation = headquartersLocation

    def getNumEmployees(self):
        return self.__numEmployees

    def setNumEmployees(self, numEmployees):
        self.__numEmployees = numEmployees

    def getOfficialWebsite(self):
        return self.__officialWebsite

    def setOfficialWebsite(self, officialWebsite):
        self.__officialWebsite = officialWebsite

    def getOfficialWebsiteLabel(self):
        return self.__officialWebsiteLabel

    def setOfficialWebsiteLabel(self, officialWebsiteLabel):
        self.__officialWebsiteLabel = officialWebsiteLabel

    def getISNI(self):
        return self.__ISNI

    def setISNI(self, ISNI):
        self.__ISNI = ISNI

    def getGRID(self):
        return self.__GRID

    def setGRID(self, GRID):
        self.__GRID = GRID

    def getQuoraTopicID(self):
        return self.__quoraTopicID

    def setQuoraTopicID(self, quoraTopicID):
        self.__quoraTopicID = quoraTopicID

    def getTwitterUsername(self):
        return self.__twitterUsername

    def setTwitterUsername(self, twitterUsername):
        self.__twitterUsername = twitterUsername


if __name__ == '__main__':
    instance = InstanceOf(QID='Q4564', label='Gomez')
    logger.debug(instance)
