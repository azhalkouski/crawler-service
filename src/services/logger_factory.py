import logging


LOG_FORMAT = '%(levelname)s:%(name)s:%(asctime)s:%(message)s'


class LoggerFactory:
    def __init__(self, base_name):
        formatter = logging.Formatter(LOG_FORMAT)

        info_logger = logging.getLogger(base_name + '.info')
        error_logger = logging.getLogger(base_name + '.error')
        critical_logger = logging.getLogger(base_name + '.critical')

        info_logger_handler = logging.FileHandler(
            filename='logs/info_level_logs.log', encoding='utf-8')
        info_logger_handler.setFormatter(formatter)

        error_logger_handler = logging.FileHandler(
            filename='logs/error_level_logs.log', encoding='utf-8')
        error_logger_handler.setFormatter(formatter)

        critical_logger_handler = logging.FileHandler(
            filename='logs/critical_level_logs.log', encoding='utf-8')
        critical_logger_handler.setFormatter(formatter)

        info_logger.addHandler(info_logger_handler)
        info_logger.setLevel(logging.INFO)

        error_logger.addHandler(error_logger_handler)
        error_logger.setLevel(logging.ERROR)

        critical_logger.addHandler(critical_logger_handler)
        critical_logger.setLevel(logging.CRITICAL)

        self.info_logger = info_logger
        self.error_logger = error_logger
        self.critical_logger = critical_logger