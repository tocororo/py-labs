from Class.instanceOf import InstanceOf
from Database.cursorPool import CursorPool
from logger_base import logger


class InstanceOfDao:
    '''
    DAO (Data Access Object) 
    CRUD: Create-Read-Update-Delete entidad instance
    '''
    __CREATE = 'CREATE TABLE IF NOT EXISTS "infoInstanceOf" AS SELECT * FROM "instanceOf";'
    __SELECT = 'SELECT * FROM "instanceOf";'
    __INSERT = 'INSERT INTO "instanceOf"(qid, label, "instanceOf") VALUES(%s,%s,%s)'
    __UPDATE = """UPDATE public."instanceOf" SET description=%s, "instanceOfLabel"=%s, image=%s, inception=%s, "nativeLabel"=%s, "foundedBy"=%s, "foundedByLabel"=%s, country=%s, "countryLabel"=%s, state=%s, "stateLabel"=%s, region=%s, "regionLabel"=%s, "headquartersLocation"=%s, "numEmployees"=%s, "officialWebsite"=%s, "officialWebsiteLabel"=%s, "ISNI"=%s, "GRID"=%s, "quoraTopicID"=%s, "twitterUsername"=%s
                   WHERE qid=%s and "instanceOfLabel" IS null """
    __UPDATE_COPY = """UPDATE public."infoInstanceOf" SET description=%s, "instanceOfLabel"=%s, image=%s, inception=%s, "nativeLabel"=%s, "foundedBy"=%s, "foundedByLabel"=%s, country=%s, "countryLabel"=%s, state=%s, "stateLabel"=%s, region=%s, "regionLabel"=%s, "headquartersLocation"=%s, "numEmployees"=%s, "officialWebsite"=%s, "officialWebsiteLabel"=%s, "ISNI"=%s, "GRID"=%s, "quoraTopicID"=%s, "twitterUsername"=%s
                      WHERE qid=%s and "instanceOfLabel" IS null """

    @classmethod
    def select(cls):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__SELECT))
            cursor.execute(cls.__SELECT)
            results = cursor.fetchall()
            instances = []
            for result in results:
                instance = InstanceOf(result[0], result[1], result[2])
                instances.append(instance)
            return instances

    @classmethod
    def insert(cls, instance):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__INSERT))
            logger.debug(f'instance to insert: {instance}')
            values = (instance.getQID(), instance.getItemLabel(), instance.getInstanceOf())
            cursor.execute(cls.__INSERT, values)
            return cursor.rowcount

    @classmethod
    def createTableInfo(cls):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__CREATE))
            cursor.execute(cls.__CREATE)
            return cursor.rowcount

    @classmethod
    def update(cls, instance):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__UPDATE))
            logger.debug(f'instance to update: {instance.getQID()}')
            values = (instance.getDescription(), instance.getInstanceOfLabel(), instance.getImage(),
                      instance.getInception(), instance.getNativeLabel(), instance.getFoundedBy(),
                      instance.getFoundedByLabel(), instance.getCountry(), instance.getCountryLabel(),
                      instance.getState(), instance.getStateLabel(), instance.getRegion(),
                      instance.getRegionLabel(), instance.getHeadquartersLocation(),
                      instance.getNumEmployees(), instance.getOfficialWebsite(),
                      instance.getOfficialWebsiteLabel(), instance.getISNI(), instance.getGRID(),
                      instance.getQuoraTopicID(), instance.getTwitterUsername(), instance.getQID())
            cursor.execute(cls.__UPDATE, values)
            return cursor.rowcount

    @classmethod
    def updateCopy(cls, instance):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__UPDATE_COPY))
            logger.debug(f'instance to update: {instance.getQID()}')
            values = (instance.getDescription(), instance.getInstanceOfLabel(), instance.getImage(),
                      instance.getInception(), instance.getNativeLabel(), instance.getFoundedBy(),
                      instance.getFoundedByLabel(), instance.getCountry(), instance.getCountryLabel(),
                      instance.getState(), instance.getStateLabel(), instance.getRegion(),
                      instance.getRegionLabel(), instance.getHeadquartersLocation(),
                      instance.getNumEmployees(), instance.getOfficialWebsite(),
                      instance.getOfficialWebsiteLabel(), instance.getISNI(), instance.getGRID(),
                      instance.getQuoraTopicID(), instance.getTwitterUsername(), instance.getQID())
            cursor.execute(cls.__UPDATE, values)
            return cursor.rowcount


if __name__ == '__main__':
    instances = InstanceOfDao.select()
    for instance in instances:
        logger.debug(instance)
        logger.debug(instance.getQID())

    # Insertamos un nuevo registro
    # instance = InstanceOf(QID='Q525', label='Najera', id_subClass='Q566')
    # inserted_instances = InstanceOfDao.insert(instance)
    # logger.debug(f'Inserted persons: {inserted_instances}')
