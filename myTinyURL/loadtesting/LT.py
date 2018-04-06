from optparse import OptionParser
from WorkLoad import WorkLoad
from Config import Config
from Reporter import Reporter
from MyLogger import logger


def main():
    logger.info('Start running loadtest')
    parser = OptionParser()
    parser.add_option("--config", dest="config", default="config.json")

    (options, args) = parser.parse_args()

    config = Config()
    config.loadFromFile(options.config)
    logger.info('Loadtest config: \n{}'.format(str(config)))


    logger.info('Start running workload')
    workload = WorkLoad(config)
    # Execute workload in a worker thread
    # since reporter must run in main thread
    workload.start()

    # Note: report must be running as the
    # last one since it blocks the main thread
    logger.info('Start running reporter')
    reporter = Reporter(config)
    reporter.run()


if __name__ == "__main__":
    main()
    input("Press Enter to continue ...")
