__license__ = "GNU General Public License v3"
__author__ = 'Hwaipy'
__email__ = 'hwaipy@gmail.com'

from interactionfreepy import IFLoop, IFWorker
import configparser
from interactionfreemongodb.MongoDBContext import MongoDBContext


class Config:
    def __init__(self, path):
        self.__path = path
        self.__config = configparser.ConfigParser()
        file = open(path)
        self.__config.read_file(file)
        file.close()

    def __getitem__(self, item):
        return ConfigItem(self, item, '')

    def get(self, section, option):
        return self.__config.get(section, option)


class ConfigItem:
    def __init__(self, config, section, option):
        self.__config = config
        self.__section = section
        self.__option = option

    def getOption(self, option):
        if self.__option: return ConfigItem(self.__config, self.__section, self.__path + '.' + option)
        return ConfigItem(self.__config, self.__section, option)

    def __getattr__(self, item):
        return self.getOption(item)

    def asString(self):
        return self.__config.get(self.__section, self.__option)

    def asInt(self):
        return int(self.asString())


class App:
    def __init__(self, config, serverName, timezone='utc'):
        self.config = Config(config)
        self.serverName = serverName
        self.timezone = timezone

    def start(self):
        self.mongoDBContext = MongoDBContext(self.config, timezone=self.timezone)
        self.storage = self.mongoDBContext.IFData.storage
        self.worker = IFWorker('tcp://{}:{}'.format(self.config['IFBroker'].Address.asString(), self.config['IFBroker'].Port.asInt()), self.serverName, self.storage)

    def join(self):
        IFLoop.join()


if __name__ == '__main__':
    app = App('config.ini', 'StorageApp', 'Asia/Shanghai')
    app.start()
    app.join()
