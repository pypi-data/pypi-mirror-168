from multiprocessing import freeze_support
import sys
from PySide2.QtWidgets import QApplication
from tptool.common.architecture import Architecture
from tptool.common.arguments import Arguments
from tptool.common.logger import Logger as Log
from tptool.config.configs import MinimalPython,SysConfig
from tptool.ui.mainwindow import MainWindow

TAG = "TPtool"

class TPtool:
    def __init__(self, argv=sys.argv):
        freeze_support()
        self._args = Arguments()
        self._app = QApplication(argv)

    def run(self):
        if Architecture.is_python_version(MinimalPython.major, minor=MinimalPython.minor):
            Log.i(TAG, "Starting TPtool")
            win = MainWindow(samples=self._args.get_user_samples())
            win.setWindowTitle("{} - {}".format(SysConfig.app_title, SysConfig.app_version))
            win.show()
            self._app.exec_()

            Log.i(TAG, "Finishing TPtool\n")
            win.close()
        else:
            self._fail()
        self.close()

    def close(self):
        self._app.exit()
        Log.close()
        sys.exit()

    def _fail(self):
        txt = str("TPtool requires Python {}.{} to run"
                  .format(MinimalPython.major, MinimalPython.minor))
        Log.e(TAG, txt)


if __name__ == '__main__':
    TPtool().run()
