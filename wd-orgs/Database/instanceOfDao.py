from Class.instanceOf import InstanceOf
from Database.cursorPool import CursorPool
from logger_base import logger


class InstanceOfDao:
    '''
    DAO (Data Access Object) 
    CRUD: Create-Read-Update-Delete entidad instance
    '''
    __CREATE_INSTANCE = """CREATE TABLE public."instanceOf"
                        (
                            qid character varying COLLATE pg_catalog."default" NOT NULL,
                            label character varying COLLATE pg_catalog."default",
                            "itemDescription" character varying COLLATE pg_catalog."default",
                            "instanceOf" character varying COLLATE pg_catalog."default",
                            "instanceOfLabel" character varying COLLATE pg_catalog."default",
                            image character varying COLLATE pg_catalog."default",
                            inception character varying COLLATE pg_catalog."default",
                            "nativeLabel" character varying COLLATE pg_catalog."default",
                            "foundedBy" character varying COLLATE pg_catalog."default",
                            "foundedByLabel" character varying COLLATE pg_catalog."default",
                            country character varying COLLATE pg_catalog."default",
                            "countryLabel" character varying COLLATE pg_catalog."default",
                            state character varying COLLATE pg_catalog."default",
                            "stateLabel" character varying COLLATE pg_catalog."default",
                            region character varying COLLATE pg_catalog."default",
                            "regionLabel" character varying COLLATE pg_catalog."default",
                            "headquartersLocation" character varying COLLATE pg_catalog."default",
                            "numEmployees" character varying COLLATE pg_catalog."default",
                            "officialWebsite" character varying COLLATE pg_catalog."default",
                            "officialWebsiteLabel" character varying COLLATE pg_catalog."default",
                            "ISNI" character varying COLLATE pg_catalog."default",
                            "GRID" character varying COLLATE pg_catalog."default",
                            "quoraTopicID" character varying COLLATE pg_catalog."default",
                            "twitterUsername" character varying COLLATE pg_catalog."default",
                            CONSTRAINT "instanceOf_pkey" PRIMARY KEY (qid)
                        )
                        
                        TABLESPACE pg_default;
                        
                        CREATE OR REPLACE FUNCTION public."before_insert_instanceofFUNs"()
                            RETURNS trigger
                            LANGUAGE 'plpgsql'
                            VOLATILE
                            COST 100
                        AS $BODY$
                        BEGIN
                             if EXISTS (select qid FROM "instanceOf" WHERE qid = new.qid ) then 
                                RETURN NULL;
                             else
                                RETURN NEW;
                            end if;
                        END;
                        $BODY$;
                        
                        CREATE TRIGGER before_insert_instanceofs
                            BEFORE INSERT
                            ON public."instanceOfs"
                            FOR EACH ROW
                            EXECUTE PROCEDURE public."before_insert_instanceofFUN"();"""

    __CREATE_SUBCLASS = """CREATE TABLE public."subClass"
                        (
                            qid character varying(255) COLLATE pg_catalog."default" NOT NULL,
                            label character varying(255) COLLATE pg_catalog."default",
                            CONSTRAINT "subClass_pkey" PRIMARY KEY (qid)
                        )
                        
                        TABLESPACE pg_default;
                        
                        ALTER TABLE public."subClass"
                            OWNER to postgres;
                        
                        CREATE OR REPLACE FUNCTION public."before_insert_subclassFUN"()
                            RETURNS trigger
                            LANGUAGE 'plpgsql'
                            VOLATILE
                            COST 100
                        AS $BODY$
                        BEGIN
                             if EXISTS (select qid FROM public."subClass" WHERE qid = new.qid ) then 
                                RETURN NULL;
                             else
                                RETURN NEW;
                            end if;
                        END;
                        $BODY$;
                        
                        CREATE TRIGGER before_insert_subclass
                            BEFORE INSERT
                            ON public."subClass"
                            FOR EACH ROW
                            EXECUTE PROCEDURE public."before_insert_subclassFUN"();"""

    __CREATE_COPY_INSTANCEOF = 'CREATE TABLE IF NOT EXISTS public."instanceOfCopy" AS SELECT * FROM "instanceOf";'
    __SELECT = 'SELECT * FROM public."instanceOf";'
    __INSERT = 'INSERT INTO public."instanceOf"(qid, label, "instanceOf") VALUES(%s,%s,%s);'
    __UPDATE = """UPDATE public."instanceOf" SET description=%s,
                  "instanceOf"=( CONCAT("instanceOf", ' / ', %s)), 
                  "instanceOfLabel"=( CONCAT("instanceOfLabel", ' / ', %s)),
                  image=%s, inception=%s, "nativeLabel"=%s, "foundedBy"=%s, "foundedByLabel"=%s, country=%s, "countryLabel"=%s, state=%s, "stateLabel"=%s, region=%s, "regionLabel"=%s, "headquartersLocation"=%s, "numEmployees"=%s, "officialWebsite"=%s, "officialWebsiteLabel"=%s, "ISNI"=%s, "GRID"=%s, "quoraTopicID"=%s, "twitterUsername"=%s
                 WHERE qid=%s; """

    __UPDATE_COPY = """UPDATE public."infoInstanceOf" SET description=%s,
                      "instanceOf"=( CONCAT("instanceOf", ' / ', %s)), 
                      "instanceOfLabel"=( CONCAT("instanceOfLabel", ' / ', %s)),
                      image=%s, inception=%s, "nativeLabel"=%s, "foundedBy"=%s, "foundedByLabel"=%s, country=%s, "countryLabel"=%s, state=%s, "stateLabel"=%s, region=%s, "regionLabel"=%s, "headquartersLocation"=%s, "numEmployees"=%s, "officialWebsite"=%s, "officialWebsiteLabel"=%s, "ISNI"=%s, "GRID"=%s, "quoraTopicID"=%s, "twitterUsername"=%s
                    WHERE qid=%s; """

    __UPDATE_FIELDS_INSTANCES_TO_NULL = """UPDATE public."instanceOf" SET "instanceOf"=NULL, "instanceOfLabel"=NULL;"""
    __UPDATE_COPY_FIELDS_INSTANCES_TO_NULL = """UPDATE public."instanceOfCopy" SET "instanceOf"=NULL, "instanceOfLabel"=NULL;"""
    __DROP_TABLES = """DROP TABLE IF EXISTS public."subClass", public."instanceOf" CASCADE;"""
    __DROP_FUNCTIONS = """DROP FUNCTiON IF EXISTS public."before_insert_instanceofFUN"(), public."before_insert_subclassFUN"() CASCADE;"""

    @classmethod
    def createTableSubclass(cls):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__CREATE_SUBCLASS))
            cursor.execute(cls.__CREATE_SUBCLASS)
            return cursor.rowcount

    @classmethod
    def createTableInstance(cls):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__CREATE_INSTANCE))
            cursor.execute(cls.__CREATE_INSTANCE)
            return cursor.rowcount

    @classmethod
    def dropTables(cls):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__DROP_TABLES))
            cursor.execute(cls.__DROP_TABLES)
            return cursor.rowcount

    @classmethod
    def dropFunctions(cls):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__DROP_FUNCTIONS))
            cursor.execute(cls.__DROP_FUNCTIONS)
            return cursor.rowcount

    @classmethod
    def createInstanceCopy(cls):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__CREATE_COPY_INSTANCEOF))
            cursor.execute(cls.__CREATE_COPY_INSTANCEOF)
            return cursor.rowcount

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
    def updateFieldsInstancesToNull(cls):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__UPDATE_FIELDS_INSTANCES_TO_NULL))
            cursor.execute(cls.__UPDATE_FIELDS_INSTANCES_TO_NULL)
            return cursor.rowcount

    @classmethod
    def updateCopyFieldsInstancesToNull(cls):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__UPDATE_COPY_FIELDS_INSTANCES_TO_NULL))
            cursor.execute(cls.__UPDATE_COPY_FIELDS_INSTANCES_TO_NULL)
            return cursor.rowcount

    @classmethod
    def update(cls, instance):
        with CursorPool() as cursor:
            logger.debug(cursor.mogrify(cls.__UPDATE))
            logger.debug(f'instance to update: {instance.getQID()}')
            print(instance.getInstanceOf())
            values = (instance.getDescription(), instance.getInstanceOf(),
                      instance.getInstanceOfLabel(), instance.getImage(),
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
            values = (instance.getDescription(), instance.getInstanceOf(),
                      instance.getInstanceOfLabel(), instance.getImage(),
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