import logging
import sys


class log:

    def __init__(self, path=None):
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter("%(asctime)s:%(name)s:%(message)s"))
        self.logger.addHandler(handler)
        if path is not None:
            pass
        self.enable_level()

    def enable_level(self, info=True, debug=False, warn=False, error=False):
        self.infol = info
        self.errorl = error
        self.warnl = warn
        self.debugl = debug

    def info(self, msg):
        if self.infol:
            self.logger.setLevel(logging.INFO)
            self.logger.info(msg)

    def debug(self, msg):
        if self.debugl:
            self.logger.setLevel(logging.DEBUG)
            self.logger.info(msg)

    def error(self, msg):
        if self.errorl:
            self.logger.setLevel(logging.ERROR)
            self.logger.info(msg)

    def warn(self, msg):
        if self.warnl:
            self.logger.setLevel(logging.WARN)
            self.logger.info(msg)
