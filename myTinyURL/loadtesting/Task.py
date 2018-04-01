import logging
from HttpConn import SyncHttpConn

class Task(object):
    def __init__(self, id, param, result_queue):
        self.id = id
        self.param = param
        self.result_queue = result_queue

    def execute(self):
        logging.info('Running task: {}'.format(self.id))
        if self.param['type'] == 'read':
            result = self.readTask()
        elif self.param['type'] == 'write':
            result = self.writeTask()
        else:
            logging.error('Unsupported task type {}'.format(self.param['type']))
        self.genResult(result)

    def genResult(self, result):
        self.result_queue.put(result)

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