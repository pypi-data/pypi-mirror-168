import multiprocessing
from time import sleep

from tptool.config.configs import SysConfig
from tptool.common.logger import Logger as Log


TAG = "Parser"


class ParserProcess(multiprocessing.Process):
    """
    Process to parse incoming data, parse it, and then distribute it to graph and storage.
    """
    def __init__(self, passer_in_queue, passer_out_queue, trigger_config_queue, store_queue=None,
                 split=SysConfig.csv_delimiter,
                 consumer_timeout=SysConfig.parser_timeout_s):
        """

        :param passer_out_queue: Reference to Queue where processed data will be put.
        :type passer_out_queue: multiprocessing Queue.
        :param store_queue: Reference to store queue instance, if needed.
        :type store_queue: store queue (multiprocessing.Process)
        :param split: Delimiter in incoming data.
        :type split: str.
        :param consumer_timeout: Time to wait after emptying the internal buffer before next parsing.
        :type consumer_timeout: float.
        """
        multiprocessing.Process.__init__(self)
        self._exit = multiprocessing.Event()
        self._in_queue = passer_in_queue
        self._out_queue = passer_out_queue
        self._trigger_config_queue = trigger_config_queue
        self._consumer_timeout = consumer_timeout
        self._split = split
        self._store_queue = store_queue
        Log.d(TAG, "Process ready")

    def run(self):
        """
        Process will monitor the internal buffer to parse raw data and distribute to graph and storage, if needed.
        The process will loop again after timeout if more data is available.
        :return:
        """
        Log.d(TAG, "Process starting...")
        while not self._exit.is_set():
            self._consume_queue()
            sleep(self._consumer_timeout)
        # last check on the queue to completely remove data.
        self._consume_queue()
        Log.d(TAG, "Process finished")

    # A string that is used to identify the type of data.
    def stop(self):
        """
        Signals the process to stop parsing data.
        :return:
        """
        Log.d(TAG, "Process finishing...")
        self._exit.set()

    def _consume_queue(self):
        """
        Consumer method for the queues/process.
        Used in run method to recall after a stop is requested, to ensure queue is emptied.
        :return:
        """
        while not self._in_queue.empty():
            queue = self._in_queue.get(timeout=self._consumer_timeout)
            self._parse_csv(queue[0], queue[1])

    def _parse_csv(self, time, line):
        """
        Parses incoming data and distributes to external processes.
        :param time: Timestamp.
        :type time: float.
        :param line: Raw data coming from acquisition process.
        :type line: basestring.
        :return:
        """
        if len(line) > 0:
            try:
                trigger_values = None
                data_values = None
                if type(line) == bytes:
                    #only parse online
                    values_str = line.decode("UTF-8")
                    values = values_str.splitlines()
                    values_str = values[0]
                    values_list = values_str.split(self._split)
                elif type(line) == str:
                    values = line.splitlines()
                    values_str = values[0]
                    values_list = values_str.split(self._split)
                else:
                    raise TypeError
                if values_list[0] == SysConfig.table_format[0]:
                    Log.i(TAG,"data value table:\n")
                    Log.i(TAG,", ".join(values_list))
                elif values_list[0] == SysConfig.data_format[0] and len(values_list) == len(SysConfig.data_format):
                    data_values = [float(v) for v in values_list[SysConfig.data_data_index:SysConfig.data_data_index+3]]
                elif values_list[0] == SysConfig.table_trigger_format[0]:
                    Log.i(TAG,"trigger table:\n")
                    Log.i(TAG,", ".join(values_list))
                elif values_list[0] == SysConfig.trigger_format[0] and len(values_list) == len(SysConfig.trigger_format):
                    trigger_values = values_list
                    Log.d(TAG,", ".join(values_list))
                elif values_list[0] == SysConfig.config_format[0] and len(values_list) == len(SysConfig.config_format):
                    trigger_values = values_list
                    Log.d(TAG,", ".join(values_list))
                else:
                    return
                if trigger_values is not None:
                    self._trigger_config_queue.put(trigger_values)
                if data_values is not None:
                    channel = int(values_list[SysConfig.data_channel_index])
                    time = float(values_list[SysConfig.data_time_index])
                    self._out_queue.put((time, channel, data_values))
                if self._store_queue is not None:
                    array = []
                    for value in values_list:
                        array.append(value)
                    #store all raw value in csv
                    self._store_queue.put(array)
            except UnicodeDecodeError:
                Log.w(TAG, "Can't decode unicode. Raw: {}".format(line.strip()))
            except ValueError:
                Log.w(TAG, "Can't convert to float. Raw: {}".format(line.strip()))
            except AttributeError:
                Log.w(TAG, "Attribute error on type ({}). Raw: {}".format(type(line), line.strip()))

