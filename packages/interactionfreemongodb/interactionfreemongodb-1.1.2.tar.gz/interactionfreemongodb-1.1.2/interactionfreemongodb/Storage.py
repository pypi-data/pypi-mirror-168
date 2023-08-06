__license__ = "GNU General Public License v3"
__author__ = 'Hwaipy'
__email__ = 'hwaipy@gmail.com'

import time
from datetime import datetime
from bson.objectid import ObjectId
from bson.codec_options import CodecOptions
import pytz
from motor.motor_tornado import MotorGridFSBucket

class Storage:
    Data = 'Data'
    RecordTime = 'RecordTime'
    FetchTime = 'FetchTime'
    Key = 'Key'

    def __init__(self, db, timezone='utc'):
        self.db = db
        self.tz = pytz.timezone(timezone)
        self.existCollections = None

    async def append(self, collection, data, fetchTime=None):
        await self.__beforeModify(collection)
        recordTime = datetime.fromtimestamp(time.time(), tz=self.tz)
        s = {
            Storage.RecordTime: recordTime,
            Storage.Data: data
        }
        if fetchTime:
            s[Storage.FetchTime] = self.__parseFetchTime(fetchTime)
        else:
            s[Storage.FetchTime] = recordTime
        r = await self.__collection(collection).insert_one(s)
        return str(r.inserted_id)

    async def latest(self, collection, by=FetchTime, after=None, filter={}, length=1):
        dbFilter = self.__reformFilter(filter)
        r = (await self.__collection(collection).find({}, dbFilter).sort(by, -1).to_list(length))
        r = [self.__reformResult(item) for item in r if ((not after) or (datetime.fromisoformat(after) < item[Storage.FetchTime]))]
        if len(r) == 0: return None
        if len(r) == 1: return r[0]
        return r

    async def first(self, collection, by=FetchTime, after=None, filter={}, length=1):
        dbFilter = self.__reformFilter(filter)
        condition = {by: {"$gt": datetime.fromisoformat(after)}} if after else {}
        r = (await self.__collection(collection).find(condition, dbFilter).sort(by, 1).to_list(length))
        r = [self.__reformResult(item) for item in r if ((not after) or (datetime.fromisoformat(after) < item[Storage.FetchTime]))]
        if len(r) == 0: return None
        if len(r) == 1: return r[0]
        return r

    async def range(self, collection, begin, end, by=FetchTime, filter={}, limit=1000):
        if by == Storage.RecordTime or by == Storage.FetchTime:
            begin = datetime.fromisoformat(begin)
            end = datetime.fromisoformat(end)
        dbFilter = self.__reformFilter(filter)
        r = await self.__collection(collection).find({"$and": [{by: {"$gt": begin}}, {by: {"$lt": end}}]}, dbFilter).to_list(length=limit)
        r.sort(key=lambda e: e[Storage.FetchTime])
        return [self.__reformResult(item) for item in r]

    async def get(self, collection, value, key='_id', filter={}):
        dbFilter = self.__reformFilter(filter)
        if key == '_id':
            value = ObjectId(value)
        if key == 'FetchTime':
            value = datetime.fromisoformat(value)
        r = (await self.__collection(collection).find({key: value}, dbFilter).to_list(length=1))
        if len(r) > 0:
            return self.__reformResult(r[0])
        else:
            return None

    async def delete(self, collection, value, key='_id'):
        await self.__beforeModify(collection)
        if key == '_id':
            value = ObjectId(value)
        if key == 'FetchTime':
            value = datetime.fromisoformat(value)
        await self.__collection(collection).delete_one({key: value})

    async def update(self, collection, id, value):
        await self.__beforeModify(collection)
        await self.__collection(collection).update_one({'_id': ObjectId(id)}, {'$set': value})

    async def createFile(self, collection):
        fsb = MotorGridFSBucket(self.db, bucket_name=f'Storage_{collection}')
        fsin = fsb.open_upload_stream(filename='', metadata={})
        id = fsin._id
        await fsin.close()
        await self.__collection(f'{collection}.files').update_one({'_id': id}, {'$set': {'chunkNum': 0}})
        return str(id)

    async def appendToFile(self, collection, fileId, data):
        if isinstance(fileId, str): fileId = ObjectId(fileId)
        colFiles = self.__collection(f'{collection}.files')
        colChunks = self.__collection(f'{collection}.chunks')

        file = (await colFiles.find({'_id': fileId}, {'_id': 1, 'length': 1, 'chunkNum': 1}).to_list(length=1))
        if len(file) == 0:
            raise ValueError(f'No file entry found: {fileId}')
        file = file[0]
        file['length'] += len(data)
        if not file.__contains__('chunkNum'): file['chunkNum'] = 0
        file['chunkNum'] += 1
        operators = [colFiles.update_one({'_id': fileId}, {'$set': file}), colChunks.insert_one({'files_id': fileId, 'n': file['chunkNum'] - 1, 'data': data, 'length': len(data)})]
        for o in operators: await o

    async def writeAChunk(self, collection, fileId, chunkNum, data):
        if isinstance(fileId, str): fileId = ObjectId(fileId)
        colFiles = self.__collection(f'{collection}.files')
        colChunks = self.__collection(f'{collection}.chunks')

        file = colFiles.find({'_id': fileId}, {'_id': 1, 'length': 1, 'chunkNum': 1}).to_list(length=1)
        chunk = colChunks.find({'files_id': fileId, 'n': chunkNum}, {'_id': 1, 'length': 1, 'n': 1}).to_list(length=1)
        file = await file
        if len(file) == 0:
            raise ValueError(f'No file entry found: {fileId}')
        file = file[0]
        if chunkNum > file['chunkNum']:
            raise ValueError(f'ChunkNum not continues during write Chunk: try to write No.{chunkNum} after No.{file["chunkNum"] - 1}.')
        chunk = await chunk
        entry = {'files_id': fileId, 'n': chunkNum, 'data': data, 'length': len(data)}
        operators = []
        if len(chunk) == 0:
            operators.append(colChunks.insert_one(entry))
        else:
            operators.append(colChunks.update_one({'files_id': fileId, 'n': chunkNum}, {'$set': entry}))
            file['length'] -= chunk[0]['length']
        file['length'] += len(data)
        file['chunkNum'] = max(file['chunkNum'], chunkNum + 1)
        operators.append(colFiles.update_one({'_id': fileId}, {'$set': file}))
        for o in operators: await o


    async def getFileMeta(self, collection, fileId):
        if isinstance(fileId, str): fileId = ObjectId(fileId)
        file = (await self.__collection(f'{collection}.files').find({'_id': fileId}, {'_id': 1, 'length': 1, 'chunkNum': 1}).to_list(length=1))
        if len(file) == 0:
            raise ValueError(f'No file entry found: {fileId}')
        return self.__reformResult(file[0])

    async def readAChunk(self, collection, fileId, chunkNum):
        if isinstance(fileId, str): fileId = ObjectId(fileId)
        chunk = (await self.__collection(f'{collection}.chunks').find({'files_id': fileId, 'n': chunkNum}, {'data': 1}).to_list(length=1))
        if len(chunk) == 0:
            raise ValueError(f'No file entry found: {fileId}')
        return chunk[0]['data']

    def __collection(self, collection):
        return self.db['Storage_{}'.format(collection)].with_options(
            codec_options=CodecOptions(tz_aware=True, tzinfo=self.tz))

    def __reformResult(self, result):
        if result.__contains__(Storage.RecordTime):
            result[Storage.RecordTime] = result[Storage.RecordTime].isoformat()
        if result.__contains__(Storage.FetchTime):
            result[Storage.FetchTime] = result[Storage.FetchTime].isoformat()
        if result.__contains__('_id'):
            result['_id'] = str(result['_id'])
        return result

    def __reformFilter(self, filter):
        if filter == {}:
            dbFilter = {}
        else:
            dbFilter = {Storage.FetchTime: 1, '_id': 1}
            dbFilter.update(filter)
        return dbFilter

    def __parseFetchTime(self, fetchTime):
        if isinstance(fetchTime, int):
            return datetime.fromtimestamp(fetchTime / 1000.0, tz=self.tz)
        elif isinstance(fetchTime, float):
            return datetime.fromtimestamp(fetchTime, tz=self.tz)
        elif isinstance(fetchTime, str):
            return datetime.fromisoformat(fetchTime)
        else:
            raise RuntimeError('FetchTime not recognized.')

    async def __senseExistCollections(self):
        self.existCollections = [c[8:] for c in await self.db.list_collection_names() if c.startswith('Storage_')]

    async def __beforeModify(self, collection):
        if self.existCollections == None:
            await self.__senseExistCollections()
        if not self.existCollections.__contains__(collection):
            await self.__collection(collection).create_index('FetchTime')
            await self.__collection(collection).create_index('RecordTime')
            self.existCollections.append(collection)


if __name__ == '__main__':
    from motor import MotorClient

    async def testFunc():
        motor = MotorClient('mongodb://IFDataAdmin:fwaejio8798fwjoiewf@172.16.60.200:27017/IFData')
        storage = Storage(motor.IFData)
        # get = await storage.append('DBTest', {'a': 'b'}, '2020-07-25T15:37:45.318000+08:00')
        print(('get'))
        get = await storage.append('SecretDebug', {'a':'b'})
        print((get))


    import asyncio
    while True:
        time.sleep(1)
        asyncio.get_event_loop().run_until_complete(testFunc())
