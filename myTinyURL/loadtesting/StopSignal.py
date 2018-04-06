from atomic import AtomicLong

class StopSignal(object):
    stop_workers = AtomicLong(0)