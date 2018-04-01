import queue
import time
import logging
import random, string

from WorkerManager import WorkerManager
from Task import Task

logging.getLogger().setLevel(logging.DEBUG)

class WorkLoad(object):
    def __init__(self, config):
        self.config = config

    # Follow steps to execute
    # 1. Create task queue and result queue
    # 2. Create worker thread pool
    # 3. Start worker threads
    # 4. Start to create tasks based on config
    # 5. Running ...
    # 6. Wait for all tasks being executed by checking result list
    def execute(self):
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()

        self.worker_mgr = WorkerManager(self.config.getWorkerNum(), self.task_queue)
        self.worker_mgr.execute()
        self.createTasks()
        logging.info('result size {}'.format(self.task_queue.qsize()))
        while self.getTotalTask() != self.result_queue.qsize():
            logging.debug('Task still running {}/{}. Waiting for another 3 seconds'.format(
                self.result_queue.qsize(), self.getTotalTask()
            ))
            time.sleep(3)
        return self.genResult()

    def genResult(self):
        return self.result_queue

    def createTasks(self):
        choice = self.weight_choice()
        task_id = 0
        for nth_sec in range(self.config.getRuntime()):
            logging.info('Creating tasks at {} sec'.format(nth_sec))
            for ith_task in range(self.config.getQPS()):
                logging.info('Creating tasks {}'.format(task_id))
                task_type = random.choice(choice)
                task_id = task_id + 1
                task = self.createTask(task_id, task_type)
                self.task_queue.put(task)
            time.sleep(1)

    def createTask(self, id, taskType):
        # TODO: create specific task and its config
        param = {}
        # def sendShort2Long(self, hostname, index_url, short_id):
        # sendLong2Short(self, hostname, index_url, convert_url, long_url)
        hostname = self.config.getHostname()
        char_candidates = string.digits
        short_id = ''.join(
            random.choice(char_candidates)
            for i in range(2)
        )
        index_url = self.config.getIndexUrl()
        convert_url = self.config.getConvertUrl()
        short_id = str(short_id).rjust(6, '0')

        url_list = ['www.douban.com', 'www.baidu.com',
                    'www.google.com', 'www.facebook.com']
        long_url = random.choice(url_list)

        if taskType == 'read':
            param = {"type":taskType, "hostname":hostname, "index_url":index_url, "short_id":short_id}
        elif taskType == 'write':
            param = {"type":taskType, "hostname":hostname, "index_url":index_url,
                     "convert_url":convert_url, "long_url":long_url}
        else:
            logging.error('Unsupported task type {}'.format(taskType))

        return Task(id, param, self.result_queue)

    def weight_choice(self):
        task_list = ['read', 'write']
        ret_list = []
        for task in task_list:
            for t in range(self.config.getWeight()[task]):
                ret_list.append(task)
        return ret_list

    def getTotalTask(self):
        return self.config.getQPS() * self.config.getRuntime()