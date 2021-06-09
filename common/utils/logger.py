from datetime import datetime
import os
import logging


def get_logger(logger_name, filename):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    log_file_path = '../{}/{}/{}.log'.format("logs", datetime.now().strftime("%Y/%m/%d"), filename)
    d = os.path.dirname(log_file_path)
    if not os.path.exists(d):
        os.makedirs(d)
    ch = logging.FileHandler(log_file_path)
    formatter = logging.Formatter("%(name)s - %(levelname)s - [%(asctime)s]: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
