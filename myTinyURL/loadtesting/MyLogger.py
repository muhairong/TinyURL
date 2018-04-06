import logging

# create logger with 'spam_application'
logger = logging.getLogger('LT')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('LT.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(filename)18s:%(lineno)3s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)