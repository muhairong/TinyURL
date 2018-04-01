class Config(object):
    def __init__(self):
        self.weight = []
        self.qps = 10
        self.runtime = 10
        self.worker_num = 3
        self.hostname = 'http://127.0.0.1:8000'
        self.convert_url = '/convert/shorten'
        self.index_url = '/convert/'

    def loadFromFile(self, filename):
        f = open(filename, 'r')
        w = list(map(int, f.readline().split(',')))
        self.weight = {'read':w[0], 'write':w[1]}
        self.qps = eval(f.readline())
        self.runtime = eval(f.readline())
        self.worker_num = eval(f.readline())
        f.close()

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
