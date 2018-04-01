from optparse import OptionParser
from WorkLoad import WorkLoad
from Config import Config
from Reporter import Reporter

def main():
    parser = OptionParser()
    parser.add_option("-c", dest="hostname", default='http://127.0.0.1:8000')
    parser.add_option("-u", "--url", dest='url', default='/convert')
    parser.add_option("--short_url", dest="short_url", default='/000002')

    (options, args) = parser.parse_args()

    config = Config()
    config.loadFromFile('testconfig')
    workload = WorkLoad(config)
    result = workload.execute()
    reporter = Reporter()
    report = reporter.genReport(result)
    print(report)

if __name__ == "__main__":
    main()