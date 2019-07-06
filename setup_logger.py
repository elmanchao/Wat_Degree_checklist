import logging


class SetupLogger:
    def __init__(self, log_file_name, print_to_screen=False):
        self.log_file_name = 'logs/'+log_file_name
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        fh = logging.FileHandler(self.log_file_name)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        if print_to_screen:
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def info(self, log_info):
        self.logger.info(log_info)

    def debug(self, debug_log):
        self.logger.debug(debug_log)

    def critical(self, critical_log):
        self.logger.critical(critical_log)

    def error(self, error_log):
        self.logger.error(error_log)

    def warning(self, warning_log):
        self.logger.warning(warning_log)
