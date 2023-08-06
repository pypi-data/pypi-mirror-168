# __license__ = "GNU General Public License v3"
# __author__ = 'Hwaipy'
# __email__ = 'hwaipy@gmail.com'

from motor.motor_tornado import MotorClient
from interactionfreemongodb.Storage import Storage


class IFConfigContext:
    def __init__(self, db, timezone):
        self.db = db
        self.storage = Storage(db, timezone)


class IFDataContext:
    def __init__(self, db, timezone):
        self.db = db
        self.storage = Storage(db, timezone)

class MongoDBContext:
    def __init__(self, config, isTest=False, timezone='utc'):
        self.__IFConfigClient = MotorClient('mongodb://{username}:{password}@{address}:{port}/{database}'.format(
            username=config['MongoDB.IFConfig'].Username.asString(),
            password=config['MongoDB.IFConfig'].Password.asString(),
            address=config['MongoDB'].Address.asString(),
            port=config['MongoDB'].Port.asInt(),
            database=config['MongoDB.IFConfig'].DB.asString(),
        ))
        self.__IFConfig = self.__IFConfigClient.get_database('IFConfig')
        if isTest:
            self.__IFConfig = self.__IFConfigClient.get_database('IFConfigTest')
        self.__IFDataClient = MotorClient('mongodb://{username}:{password}@{address}:{port}/{database}'.format(
            username=config['MongoDB.IFData'].Username.asString(),
            password=config['MongoDB.IFData'].Password.asString(),
            address=config['MongoDB'].Address.asString(),
            port=config['MongoDB'].Port.asInt(),
            database=config['MongoDB.IFData'].DB.asString(),
        ))
        self.__IFData = self.__IFDataClient.get_database('IFData')
        if isTest:
            self.__IFData = self.__IFDataClient.get_database('IFDataTest')
        self.IFConfig = IFConfigContext(self.__IFConfig, timezone)
        self.IFData = IFDataContext(self.__IFData, timezone)

        # print('mongodb://{username}:{password}@{address}:{port}/{database}'.format(
        #     username=config['MongoDB.IFConfig'].Username.asString(),
        #     password=config['MongoDB.IFConfig'].Password.asString(),
        #     address=config['MongoDB'].Address.asString(),
        #     port=config['MongoDB'].Port.asInt(),
        #     database=config['MongoDB'].DB
        # ))