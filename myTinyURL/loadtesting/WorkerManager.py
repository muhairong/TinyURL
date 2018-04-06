import threading
import queue
from MyLogger import logger
from StopSignal import StopSignal
from Stat import Stat

class Worker(threading.Thread):
    def __init__(self, workerID):
        threading.Thread.__init__(self)
        self.id = workerID

    def run(self):
        while True:
            stop = StopSignal.stop_workers.value
            if stop:
                break
            try:
                task = Stat.task_queue.get(block=True, timeout=3)
            except queue.Empty:
                continue
            logger.info('Worker {} is executing task {}'.format(self.id, task.id))
            task.execute()
        logger.info("Worker stopped: {}".format(self.id))

class WorkerManager(object):
    def __init__(self, workerNum):
        self.worker_num = workerNum
        logger.info('Creating {} workers'.format(self.worker_num))
        self.workers = []
        for i in range(self.worker_num):
            worker = Worker(i)
            self.workers.append(worker)

    def execute(self):
        for worker in self.workers:
            worker.start()

