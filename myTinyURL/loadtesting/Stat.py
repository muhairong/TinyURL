from atomic import AtomicLong
import queue


class Stat(object):
    gen_tasks = AtomicLong(0)
    finished_tasks = AtomicLong(0)
    task_queue = queue.Queue()
    # Each result contains several fields
    # 1. TaskID
    # 2. TimePoints: create time, send time, response time
    # 3. Succ
    result_queue = queue.Queue()