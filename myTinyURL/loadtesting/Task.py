from MyLogger import logger
from HttpConn import SyncHttpConn
from Stat import Stat
import time

class Task(object):
    def __init__(self, id, param):
        self.id = id
        self.param = param
        self.create_time = time.time()

    def execute(self):
        logger.info('Running task: {}'.format(self.id))
        self.send_time = time.time()
        if self.param['type'] == 'read':
            result = self.readTask()
        elif self.param['type'] == 'write':
            result = self.writeTask()
        else:
            logger.error('Unsupported task type {}'.format(self.param['type']))
        self.response_time = time.time()

        Stat.finished_tasks += 1
        task_stat = {
            'id': self.id,
            'type': self.param['type'],
            'create_time': self.create_time,
            'send_time': self.send_time,
            'response_time': self.response_time,
            'succ': result['succ'],
        }
        Stat.result_queue.put(task_stat)

    def readTask(self):
        request = SyncHttpConn()
        # def sendShort2Long(self, hostname, index_url, short_url):
        request.sendShort2Long(self.param['hostname'], self.param['index_url'], self.param['short_id'])
        return request.getResult()

    def writeTask(self):
        request = SyncHttpConn()
        # sendLong2Short(self, hostname, index_url, convert_url, long_url)
        request.sendLong2Short(self.param['hostname'], self.param['index_url'],
                               self.param['convert_url'], self.param['long_url'])
        return request.getResult()