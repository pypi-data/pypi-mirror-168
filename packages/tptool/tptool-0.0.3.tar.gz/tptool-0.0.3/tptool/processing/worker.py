from multiprocessing import Queue

from tptool.config.configs import SysConfig, SourceType
from tptool.processing.csv import CSVProcess
from tptool.processing.parser import ParserProcess
from tptool.processing.serial import SerialProcess
from tptool.processing.simulator import SimulatorProcess
from tptool.common.logger import Logger as Log
from tptool.common.ringbuffer import RingBuffer


TAG = "Worker"


class Worker:
    """
    Concentrates all workers (processes) to run the application.
    """
    def __init__(self,
                 port=None,
                 speed=SysConfig.serial_default_speed,
                 samples=SysConfig.samples_buffer_size,
                 source=SourceType.serial,
                 export_enabled=False,
                 export_path=SysConfig.app_export_path):
        """
        Creates and orchestrates all processes involved in data acquisition, processing and storing.
        :param port: Port to open on start.
        :type port: str.
        :param speed: Speed for the specified port (depending on source).
        :type speed: float.
        :param samples: Number of samples to keep in the buffers (should match with plot samples).
        :type samples: int.
        :param source: Source type where data should be obtained
        :type source: SourceType.
        :param export_enabled: If true, data will be stored or exported in a file.
        :type export_enabled: bool.
        :param export_path: If specified, defines where the data will be exported.
        :type export_path: str.
        """
        self._passer_out_queue = Queue()
        self._trigger_config_queue = Queue()
        self._raw_data_queue = Queue()
        self._store_queue = Queue()
        self._data_buffers = None
        self._time_buffer = None
        self._lines = 0

        self._acquisition_process = None
        self._parser_process = None
        self._passer_in_queue = Queue()
        self._command_out_queue = Queue()
        self._csv_process = None

        self._port = port
        self._speed = float(speed)
        self._samples = samples
        self._source = source
        self._export = export_enabled
        self._path = export_path
        self._retting_buffers = 0

    def start(self):
        """
        Starts all processes, based on configuration given in constructor.
        :return:
        """
        self.reset_buffers(self._samples)
        if self._export:
            self._csv_process = CSVProcess(self._store_queue, path=self._path)
            self._parser_process = ParserProcess(self._passer_in_queue, self._passer_out_queue, self._trigger_config_queue, store_queue=self._store_queue)
        else:
            self._parser_process = ParserProcess(self._passer_in_queue, self._passer_out_queue, self._trigger_config_queue)

        if self._source == SourceType.serial:
            self._acquisition_process = SerialProcess(self._passer_in_queue, self._command_out_queue, self._raw_data_queue)
        elif self._source == SourceType.simulator:
            self._acquisition_process = SimulatorProcess(self._passer_in_queue)
        if self._acquisition_process.open(port=self._port, speed=self._speed):
            self._parser_process.start()
            if self._export:
                self._csv_process.start()
            self._acquisition_process.start()
            return True
        else:
            Log.i(TAG, "Port is not available")
            return False

    def stop(self):
        """
        Stops all running processes.
        :return:
        """
        self.consume_queue()
        for process in [self._acquisition_process, self._parser_process, self._csv_process]:
            if process is not None and process.is_alive():
                process.stop()
                process.join(SysConfig.process_join_timeout_ms)

    def consume_queue(self):
        """
        Empties the internal queue, updating data to consumers.
        :return:
        """
        while not self._passer_out_queue.empty():
            self._load_data(self._passer_out_queue.get(False))

    def _load_data(self, data):
        """
        Adds data to internal time and data buffers.
        :param data: values to add to internal buffers.
        :type data: list.
        :return:
        """
        # 0 time, 1 channel, 2 [raw, base, smooth]
        # Add timestamp
        _time = data[0]
        _channel = int(data[1])
        if _channel < 0 or _channel > SysConfig.plot_max_channels:
            Log.e(TAG, "invalid channel number {}".format(_channel))
            return
        _values = data[2]
        self._time_buffer[_channel].append(_time)
        self._load_signal_values(_channel, _values)

    def _load_signal_values(self, channel, values):
        """
        Stores the signal values in internal buffers.
        :param values: Values to store.
        :type values: float list.
        :return:
        """
        # detect how many lines are present to plot
        # const == 3 here
        if self._retting_buffers == 1:
            return
        size = len(values)
        # if _lines < real size, we need to create more buffer
        if self._lines < size:
            if size > SysConfig.plot_max_lines:
                self._lines = SysConfig.plot_max_lines
            else:
                self._lines = size

        # store the data in respective buffers
        for idx in range(self._lines):
            self._data_buffers[channel][idx].append(values[idx])
    def send_command(self, command):
        self._command_out_queue.put(command)
    def get_time_buffer(self, channel):
        """
        Gets the complete buffer for time.
        :return: Time buffer.
        :rtype: float list.
        """
        return self._time_buffer[channel].get_partial()
    def get_raw_buffer(self):
        if self._raw_data_queue == None or self._raw_data_queue.empty():
            return []
        else:
            return self._raw_data_queue.get(False)
    def get_trigger_config_buffer(self):
        if self._trigger_config_queue.empty():
            return []
        else:
            return self._trigger_config_queue.get(False)
    def get_values_buffer(self, channel, idx=0):
        """
        Gets the complete buffer for a line data, depending on specified index.
        :param idx: Index of the line data to get.
        :type idx: int.
        :return: float list.
        """
        if self._retting_buffers == 1:
            return []
        if channel < 0 or channel > SysConfig.plot_max_channels:
            Log.e(TAG, "invalid channel number {}".format(channel))
            return []
        if idx >= SysConfig.plot_max_lines:
            Log.e(TAG, "invalid line number {}".format(idx))
            return []
        return self._data_buffers[channel][idx].get_partial()

    def get_lines(self):
        """
        Gets the current number of found lines in input data.
        :return: Current number of lines.
        :rtype: int.
        """
        return self._lines

    def is_running(self):
        """
        Checks if processes are running.
        :return: True if a process is running.
        :rtype: bool.
        """
        return self._acquisition_process is not None and self._acquisition_process.is_alive()

    @staticmethod
    def get_source_ports(source):
        """
        Gets the available ports for specified source.
        :param source: Source to get available ports.
        :type source: SourceType.
        :return: List of available ports.
        :rtype: str list.
        """
        if source == SourceType.serial:
            return SerialProcess.get_ports()
        elif source == SourceType.simulator:
            return SimulatorProcess.get_ports()
        else:
            Log.w(TAG, "Unknown source selected")
            return None

    @staticmethod
    def get_source_speeds(source):
        """
        Gets the available speeds for specified source.
        :param source: Source to get available speeds.
        :type source: SourceType.
        :return: List of available speeds.
        :rtype: str list.
        """
        if source == SourceType.serial:
            return SerialProcess.get_speeds()
        elif source == SourceType.simulator:
            return SimulatorProcess.get_speeds()
        else:
            Log.w(TAG, "Unknown source selected")
            return None

    def reset_buffers(self, samples):
        """
        Setup/clear the internal buffers.
        :param samples: Number of samples for the buffers.
        :type samples: int.
        :return:
        """
        self._retting_buffers = 1
        self._data_buffers = []
        self._time_buffer = []
        for tmp in range(0, SysConfig.plot_max_channels + 1):
            self._data_buffers.append([RingBuffer(samples), RingBuffer(samples), RingBuffer(samples)]) #TODO: using plot_max_lines for Ringbuffer create
            self._time_buffer.append(RingBuffer(samples))
        while not self._passer_out_queue.empty():
            self._passer_out_queue.get()
        Log.i(TAG, "Buffers cleared")
        self._retting_buffers = 0
