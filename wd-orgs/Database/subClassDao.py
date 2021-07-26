from Class.subClass import SubClass
from Database.cursorPool import CursorPool
from logger_base import logger


class SubClassDao:
    '''
    DAO (Data Access Object) 
    CRUD: Create-Read-Update-Delete entidad subClass
    '''
    __SELECT = 'SELECT * FROM "subClass" ;'
    __INSERT = 'INSERT INTO "subClass"(qid, label) VALUES(%s,%s)'

    @classmethod
    def select(cls):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__SELECT))
            cursor.execute(cls.__SELECT)
            results = cursor.fetchall()
            subClasses = []
            for result in results:
                subClass = SubClass(result[0], result[1])
                subClasses.append(subClass)
            return subClasses

    @classmethod
    def insert(cls, subClass):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__INSERT))
            logger.debug(f'subClass to insert: {subClass}')
            values = (subClass.getQID(), subClass.getItemLabel())
            cursor.execute(cls.__INSERT, values)
            return cursor.rowcount


if __name__ == '__main__':
    subClasses = SubClassDao.select()
    print(subClasses)
    for subClass in subClasses:
        logger.debug(subClass)
        logger.debug(subClass.getQID())

    # Insertamos un nuevo registro
    # subClass = SubClass(QID='Q525', label='Najera', id_subClass='Q566')
    # inserted_instances = InstanceOfDao.insert(subClass)
    # logger.debug(f'Inserted persons: {inserted_instances}')
