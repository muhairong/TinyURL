import http.client
import requests
import string, time, random


class HttpRequst():
    # res.status, res.reason
    # https://docs.python.org/3.5/library/http.client.html
    @classmethod
    def get(cls, url):
        """
        conn = http.client.HTTPConnection("localhost", 8000)
        conn.request("GET", url)
        response = conn.getresponse()
        return response
        """
        # url: /convert/000002/
        request = 'http://127.0.0.1:8000' + url
        response = requests.get(request)
        return response

    @classmethod
    def post(cls, url):

        """conn = http.client.HTTPConnection("localhost", 8000)
        conn.request("POST", "/convert/shorten", params, headers)
        response = conn.getresponse()
        return response
        """
        session = requests.Session()
        r = session.get('http://127.0.0.1:8000/convert')
        csrftoken = r.cookies['csrftoken']
        response = session.post("http://127.0.0.1:8000/convert/shorten",
                         {"url":url},
                         headers={'X-CSRFToken': csrftoken})
        return response


class Config(object):
    def __init__(self):
        self.weight = []
        self.qps = 10
        self.runtime = 10

    def loadFromFile(self, filename):
        f = open(filename, 'r')
        self.weight = list(map(int, f.readline().split(',')))
        self.qps = eval(f.readline())
        self.runtime = eval(f.readline())
        f.close()

    def getWeight(self):
        return self.weight

    def getQPS(self):
        return self.qps

    def getRuntime(self):
        return self.runtime


class Task():
    @classmethod
    def readSingle(cls):
        char_candidates = string.digits
        short_id = ''.join(
            random.choice(char_candidates)
            for i in range(3)
        )
        short_id = str(short_id).rjust(6, '0')
        url = '/convert/' + short_id
        return HttpRequst.get(url)

    @classmethod
    def write(cls):
        url_list = ['www.douban.com', 'www.baidu.com',
                    'www.google.com', 'www.facebook.com']
        long_url = random.choice(url_list)
        return HttpRequst.post(long_url)


class WorkLoad():
    def __init__(self, config):
        self.weight = config.getWeight()
        self.qps = config.getQPS()
        self.runtime = config.getRuntime()

    def execute(self):
        task_list = self.weight_choice()
        response_list = []
        time_limit = time.time() + self.runtime

        while time.time() < time_limit:
            for q in range(self.qps):
                task = random.choice(task_list)
                if task is 'r':
                    response = Task.readSingle()
                else:
                    response = Task.write()
                response_list.append(response)
        return response_list

    def weight_choice(self):
        task_list = ['r', 'w']
        ret_list = []
        for i, val in enumerate(task_list):
            ret_list.extend(val * self.weight[i])
        return ret_list


class Report():
    @classmethod
    def genReport(cls, result):
        pass


def main():
    print("Load testing")
    config = Config()
    config.loadFromFile('testconfig')
    w = WorkLoad(config)
    res = w.execute()
    Report.genReport(res)


if __name__ == "__main__":
    main()
