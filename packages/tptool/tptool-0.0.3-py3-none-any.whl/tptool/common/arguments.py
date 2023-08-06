import argparse
from tptool.common.logger import Logger as Log
from tptool.config.configs import SysConfig
import logging

TAG = "Arguments"


class Arguments:
    """
    Wrapper for argparse package.
    """
    def __init__(self):
        self._parser = None
        parser = argparse.ArgumentParser(description='TPtool\nESP32SX touchsensor debug tool')
        parser.add_argument("-i", "--info",
                            dest="log_level_info",
                            action='store_true',
                            help="Enable info messages"
                            )

        parser.add_argument("-d", "--debug",
                            dest="log_level_debug",
                            action='store_true',
                            help="Enable debug messages"
                            )

        parser.add_argument("-v", "--verbose",
                            dest="log_to_console",
                            action='store_true',
                            help="Show log messages in console",
                            default=SysConfig.log_default_to_console
                            )

        parser.add_argument("-s", "--samples",
                            dest="user_samples",
                            default=SysConfig.samples_buffer_size,
                            help="Specify number of sample to show on plot"
                            )
        self._parser = parser.parse_args()
        if self._parser is not None:
            self._parse_log_level()

    def get_user_samples(self):
        """
        Gets the user specified samples to show in the plot.
        :return: Samples specified by user, or default value if not specified.
        :rtype: int.
        """
        return int(self._parser.user_samples)

    def _parse_log_level(self):
        """
        Sets the log level depending on user specification.
        It will also enable or disable log to console based on user specification.
        :return:
        """
        level = logging.DEBUG if SysConfig.log_level_debug==1 else logging.INFO
        if self._parser.log_level_info:
            level = logging.INFO
        elif self._parser.log_to_console or self._parser.log_level_debug:
            level = logging.DEBUG
        Log(level, enable_console=self._parser.log_to_console)
