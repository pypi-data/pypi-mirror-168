import multiprocessing
from time import time, sleep

import serial
from serial.tools import list_ports

from tptool.common.architecture import Architecture
from tptool.common.architecture import OSType
from tptool.config.configs import SysConfig
from tptool.common.logger import Logger as Log


TAG = "Serial"


class SerialProcess(multiprocessing.Process):
    """
    Wrapper for serial package into a multiprocessing instance.
    """
    def __init__(self, out_queue, in_queue, raw_queue = None):
        """
        Initialises values for process.
        :param out_queue: Reference to a Queue instance.
        :type out_queue: Queue.
        """
        multiprocessing.Process.__init__(self)
        self._exit = multiprocessing.Event()
        self._out_queue = out_queue
        self._in_queue = in_queue
        self._raw_queue = raw_queue
        self._serial = serial.Serial()
        Log.i(TAG, "Process ready")

    def open(self, port, speed=SysConfig.serial_default_speed, timeout=SysConfig.serial_timeout_s):
        """
        Opens a specified serial port.
        :param port: Serial port name.
        :type port: str.
        :param speed: Baud rate, in bps, to connect to port.
        :type speed: int.
        :param timeout: Sets the general connection timeout.
        :type timeout: float.
        :return: True if the port is available.
        :rtype: bool.
        """
        self._serial.port = port
        self._serial.baudrate = int(speed)
        self._serial.stopbits = serial.STOPBITS_ONE
        self._serial.bytesize = serial.EIGHTBITS
        self._serial.timeout = timeout
        return self._is_port_available(self._serial.port)

    def run(self):
        """
        Reads the serial port expecting CSV until a stop call is made.
        The expected format is comma (",") separated values, and a new line (CRLF or LF) as a new row.
        While running, it will parse CSV data convert each value to float and added to a queue.
        If incoming data from serial port can't be converted to float, that data will be discarded.
        :return:
        """
        Log.i(TAG, "Process starting...")
        if self._is_port_available(self._serial.port):
            if not self._serial.isOpen():
                self._serial.open()
                Log.i(TAG, "Port opened")
                timestamp = time()
                while not self._exit.is_set():
                    serial_idel = 0
                    if self._serial.readable():
                        line = self._serial.readline()
                        self._out_queue.put([time() - timestamp, line])
                        if self._raw_queue != None:
                            self._raw_queue.put([line])
                    else:
                        serial_idel += 1
                    if not self._in_queue.empty():
                        command = self._in_queue.get()
                        command = command + "\r\n"
                        self._serial.write(command.encode('utf-8'))
                        Log.i(TAG, "command write: " + command)
                    else:
                        serial_idel += 1
                    if serial_idel == 2:
                        sleep(self._serial.timeout)
                Log.i(TAG, "Process finished")
                self._serial.close()
            else:
                Log.w(TAG, "Port is not opened")
        else:
            Log.w(TAG, "Port is not available")

    def stop(self):
        """
        Signals the process to stop acquiring data.
        :return:
        """
        Log.i(TAG, "Process finishing...")
        self._exit.set()

    @staticmethod
    def get_ports():
        """
        Gets a list of the available serial ports.
        :return: List of available serial ports.
        :rtype: str list.
        """
        if Architecture.get_os() is OSType.macosx:
            import glob
            return glob.glob("/dev/tty.*")
        else:
            found_ports = []
            for port in list(list_ports.comports()):
                Log.d(TAG, "found device {}".format(port))
                found_ports.append(port.device)
            return found_ports

    @staticmethod
    def get_speeds():
        """
        Gets a list of the common serial baud rates, in bps.
        :return: List of the common baud rates, in bps.
        :rtype: str list.
        """
        return [str(v) for v in [115200, 460800, 921600, 1000000, 1152000, 2000000]]

    def _is_port_available(self, port):
        """
        Checks is the port is currently connected to the host.
        :param port: Port name to be verified.
        :return: True if the port is connected to the host.
        :rtype: bool.
        """
        for p in self.get_ports():
            if p == port:
                return True
        return False
