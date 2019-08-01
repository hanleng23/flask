import logging
import sys

logger = logging.getLogger("server_logger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt='%(asctime)s %(filename)s %(levelname)s: %(message)s',
                              datefmt='%a, %d %b %Y %H:%M:%S')

lo = logging.StreamHandler()
lo.setLevel(logging.DEBUG)
lo.setFormatter(formatter)
logger.addHandler(lo)