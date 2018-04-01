import requests
import logging
import asyncio
from optparse import OptionParser

logging.getLogger().setLevel(logging.DEBUG)

class ConnResult():
    def __init__(self):
        self.succ = False
        self.latency = -1

class HttpConn():
    TOKENKEY = 'csrftoken'
    CSRFTOKENKEY = 'X-CSRFToken'
    def sendShort2Long(self, hostname, url):
        pass

    def sendLong2Short(self, hostname, url):
        pass

    # Return ConnResult
    def getResult(self):
        pass


class SyncHttpConn(HttpConn):
    def __init__(self):
        self.result = None

    # url must start with backslash
    def sendShort2Long(self,hostname, index_url, short_id):
        logging.debug('Sending sync get to {} with {} {}'.format(hostname, index_url, short_id))
        request = '{}{}{}'.format(hostname, index_url, short_id)
        response = requests.get(request)
        logging.debug(response)
        # TODO: check response and set result
        self.result = response

    # url must start with backslash
    def sendLong2Short(self, hostname, index_url, convert_url, long_url):
        logging.debug('Sending sync post to {} with {}'.format(hostname, long_url))
        session = requests.Session()
        r = session.get('{}{}'.format(hostname, index_url))
        csrftoken = r.cookies[HttpConn.TOKENKEY]
        response = session.post('{}{}'.format(hostname, convert_url),
                         {"url":long_url},
                         headers={HttpConn.CSRFTOKENKEY: csrftoken})
        # TODO: check response and set result
        self.result = response

    def getResult(self):
        logging.debug('Calling getResult')
"""
class AsyncHttpConn(HttpConn):
    def __init__(self):
        self.result = None

    def sendShort2Long(self, hostname, url, short_url):


    def sendLong2Short(self, hostname, index_url, convert_url, long_url):


    def getResult(self):
        logging.debug('Calling getResult')

def main():
    parser = OptionParser()
    parser.add_option("-c", dest="hostname", default='http://127.0.0.1:8000')
    parser.add_option("-u", "--url", dest='url', default='/convert')
    parser.add_option("--short_url", dest="short_url", default='/000002')

    (options, args) = parser.parse_args()
    conn = SyncHttpConn()
    conn.sendShort2Long(options.hostname, options.url, options.short_url)



if __name__ == "__main__":
    main()
"""

