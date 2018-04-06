import json
class Config(object):
    def __init__(self):
        self.weight = []
        self.qps = 10
        self.runtime = 10
        self.worker_num = 3
        self.hostname = 'http://127.0.0.1:8000'
        self.convert_url = '/convert/shorten'
        self.index_url = '/convert/'

    def __str__(self):
        return 'Weight: {}\nQPS: {}\nRuntime: {}\nWorkerNum: {}\nHostname: {}\n'.format(
            self.getWeight(), self.getQPS(), self.getRuntime(), self.getWorkerNum(), self.getHostname(),
        )

    def loadFromFile(self, filename):
        with open(filename, 'r') as f:
            config = json.load(f)
        w = []
        w.append(config['read_weight'])
        w.append(config['write_weight'])
        self.weight = {'read': w[0], 'write': w[1]}
        self.qps = config['qps']
        self.runtime = config['runtime']
        self.worker_num = config['worker_num']
        self.hostname = config['hostname']
        self.convert_url = config['convert_url']
        self.index_url = config['index_url']

    def getWeight(self):
        return self.weight

    def getQPS(self):
        return self.qps

    def getRuntime(self):
        return self.runtime

    def getWorkerNum(self):
        return self.worker_num

    def getHostname(self):
        return self.hostname

    def getConvertUrl(self):
        return self.convert_url

    def getIndexUrl(self):
        return self.index_url
