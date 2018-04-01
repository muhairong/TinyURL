import logging
import threading

class Worker(threading.Thread):
    def __init__(self, workerID, taskQueue):
        threading.Thread.__init__(self)
        self.id = workerID
        self.task_queue = taskQueue

    def run(self):
        while True:
            task = self.task_queue.get(block=True)
            logging.info('Worker {} is executing task {}'.format(self.id, task.id))
            task.execute()

class WorkerManager(object):
    def __init__(self, workerNum, taskQueue):
        self.worker_num = workerNum
        self.task_queue = taskQueue
        logging.info('Creating {} workers'.format(self.worker_num))
        self.workers = []
        for i in range(self.worker_num):
            worker = Worker(i, self.task_queue)
            self.workers.append(worker)

    def execute(self):
        for worker in self.workers:
            worker.start()

