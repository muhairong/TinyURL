import time
import random, string

from WorkerManager import WorkerManager
from Task import Task
from MyLogger import logger
from StopSignal import StopSignal
from Stat import Stat
import threading

class WorkLoad(threading.Thread):
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.config = config
        StopSignal.lock = threading.Lock()

    # Follow steps to execute
    # 1. Create task queue and result queue
    # 2. Create worker thread pool
    # 3. Start worker threads
    # 4. Start to create tasks based on config
    # 5. Running ...
    # 6. Wait for all tasks being executed by checking result list
    def run(self):
        self.worker_mgr = WorkerManager(self.config.getWorkerNum())
        self.worker_mgr.execute()
        self.createTasks()
        while self.getTotalTask() != Stat.finished_tasks.value:
            logger.info('Task still running {}/{}. Waiting for another 3 seconds'.format(
                Stat.finished_tasks.value, self.getTotalTask()
            ))
            time.sleep(3)
        logger.info('Now sleep 3 seconds and stop all workers')
        time.sleep(3)
        StopSignal.stop_workers.get_and_set(1)

    def createTasks(self):
        choice = self.weight_choice()
        task_id = 0
        for nth_sec in range(self.config.getRuntime()):
            logger.info('Creating tasks at {} sec'.format(nth_sec))
            for ith_task in range(self.config.getQPS()):
                task_type = random.choice(choice)
                task_id = task_id + 1
                logger.info('Creating tasks {}:{}'.format(task_id, task_type))
                task = self.createTask(task_id, task_type)
                Stat.gen_tasks += 1
                Stat.task_queue.put(task)
            time.sleep(1)

    def createTask(self, id, taskType):
        param = {}
        hostname = self.config.getHostname()
        char_candidates = string.digits
        short_id = ''.join(
            random.choice(char_candidates)
            for i in range(3)
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
            logger.error('Unsupported task type {}'.format(taskType))

        return Task(id, param)

    def weight_choice(self):
        task_list = ['read', 'write']
        ret_list = []
        for task in task_list:
            for t in range(self.config.getWeight()[task]):
                ret_list.append(task)
        return ret_list

    def getTotalTask(self):
        return self.config.getQPS() * self.config.getRuntime()