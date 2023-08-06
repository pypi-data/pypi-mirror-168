from ast import Constant
import imp
import numpy as np
from PySide2.QtCore import Qt
import pyqtgraph as pg
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QComboBox, QFileDialog
from time import strftime, gmtime, sleep
from tptool.ui.ui_touchmain import Ui_MainWindow
from tptool.processing.worker import Worker
from tptool.config.configs import SysConfig, SourceType, TpConfig, TpCommand
from tptool.ui.popup import PopUp
from tptool.common.logger import Logger as Log
from tptool.common.logger import Loggerlevel as Loggerlevel


TAG = "MainWindow"


class MainWindow(QMainWindow):
    """
    Handles the ui elements and connects to worker service to execute processes.
    """
    def __init__(self, port=None, bd=115200, samples=500):
        """
        Initializes values for the UI.
        :param port: Default port name to be used. It will also disable scanning available ports.
        :type port: str.
        :param bd: Default baud rate to be used. It will be added to the common baud rate list if not available.
        :type bd: int.
        :param samples: Default samples per second to be shown in the plot.
        :type samples: int.
        """
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._configure_ui()

        #TODO: 14+3, 15:TRIGGER 16:DIFF
        self._plt = [None for _ in range(0, SysConfig.plot_max_channels + 3)]
        self._plt_curve = [[None,None,None] for _ in range(0, SysConfig.plot_max_channels + 3)]
        self._plt_infi = [] #time,channel,infiobj
        self._timer_plot = None
        self._timer_table = None
        self._timer_ref = 0
        self._timer_plot_pause = 0
        self._channel_choosed_mask = 0
        self.worker = None
        self._touch_in_sleep = 0
        self._command_disabled = 0

        # configures
        self.ui.comboBox_source.addItems(SysConfig.app_sources)
        self._configure_plot()
        self._configure_timers()
        self._update_options()
        self._configure_signals()

        # populate combo box for serial ports
        self._source_changed()
        self.ui.comboBox_source.setCurrentIndex(SourceType.serial.value)

        self.ui.spin_samples.setValue(samples)

        # enable ui
        self._enable_ui(True)
        self._count_triggers = 0
        self._diff_max = [0] * (SysConfig.plot_max_channels + 1)
        self._diff_rate = [0.0] * (SysConfig.plot_max_channels + 1)
        self._diff_update_count = 0

    def start(self):
        """
        Starts the acquisition of the selected serial port.
        This function is connected to the clicked signal of the Start button.
        :return:
        """
        Log.i(TAG, "Clicked start")
        self._diff_max = [0] * (SysConfig.plot_max_channels + 1)
        self._diff_rate = [0.0] * (SysConfig.plot_max_channels + 1)
        self.worker = Worker(port=self.ui.comboBox_port.currentText(),
                             speed=float(self.ui.comboBox_portspd.currentText()),
                             samples=self.ui.spin_samples.value(),
                             source=self._get_source(),
                             export_enabled=self.ui.checkBox_file.isChecked(),
                             export_path=self.ui.lineEdit_path.text())
        if self.worker.start():
            self._enable_ui(False)
        else:
            Log.i(TAG, "Port is not available")
            PopUp.warning(self, SysConfig.app_title, "Selected port \"{}\" is not available"
                          .format(self.ui.comboBox_port.currentText()))
        self._timer_table.start()
        if self._timer_ref >= 1:
            self._timer_plot.start()
            Log.i(TAG, "Plot timmer start\n")
        self._command_enable_output()
    def stop(self):
        """
        Stops the acquisition of the selected serial port.
        This function is connected to the clicked signal of the Stop button.
        :return:
        """
        Log.i(TAG, "Clicked stop")
        self._timer_plot.stop()
        self._timer_table.stop()
        self._enable_ui(True)
        self.worker.stop()
        self.worker = None

    def closeEvent(self, evnt):
        """
        Overrides the QTCloseEvent.
        This function is connected to the clicked signal of the close button of the window.
        :param evnt: QT evnt.
        :return:
        """
        if self.worker is not None and self.worker.is_running():
            Log.i(TAG, "Window closed without stopping capture, stopping it")
            self.stop()
    def _enable_plot_chan(self, mask, enable):
        for i in range(1,15):
            if mask & (0x0001 << i):
                self.ui.buttonGroup.button(i).setEnabled(enable)
    def _configure_ui(self):
        self.ui.buttonGroup.addButton(self.ui.checkBox_1, 1)
        self.ui.buttonGroup.addButton(self.ui.checkBox_2, 2)
        self.ui.buttonGroup.addButton(self.ui.checkBox_3, 3)
        self.ui.buttonGroup.addButton(self.ui.checkBox_4, 4)
        self.ui.buttonGroup.addButton(self.ui.checkBox_5, 5)
        self.ui.buttonGroup.addButton(self.ui.checkBox_6, 6)
        self.ui.buttonGroup.addButton(self.ui.checkBox_7, 7)
        self.ui.buttonGroup.addButton(self.ui.checkBox_8, 8)
        self.ui.buttonGroup.addButton(self.ui.checkBox_9, 9)
        self.ui.buttonGroup.addButton(self.ui.checkBox_10, 10)
        self.ui.buttonGroup.addButton(self.ui.checkBox_11, 11)
        self.ui.buttonGroup.addButton(self.ui.checkBox_12, 12)
        self.ui.buttonGroup.addButton(self.ui.checkBox_13, 13)
        self.ui.buttonGroup.addButton(self.ui.checkBox_14, 14)
        #TODO can not using in esp32s3
        #self.ui.btn_deepsleep.setEnabled(False)
        self.ui.tableWidget.setColumnCount(len(SysConfig.trigger_format)-1)
        self.ui.tableWidget.setRowCount(SysConfig.trigger_table_size)
        self.ui.tableWidget.setHorizontalHeaderLabels(SysConfig.trigger_format[1:])
        self.ui.spin_samples.setMaximum(100000)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(40)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ui.tableWidget.setFont(font)
        self.ui.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

    def _enable_ui(self, enabled):
        """
        Enables or disables the UI elements of the window.
        :param enabled: The value to be set at the enabled characteristic of the UI elements.
        :type enabled: bool
        :return:
        """
        self.ui.pushButton_chiprestart.setEnabled(not enabled)
        self.ui.spin_samples_freq.setEnabled(enabled)
        self.ui.comboBox_port.setEnabled(enabled)
        self.ui.comboBox_portspd.setEnabled(enabled)
        self.ui.pushButton_start.setEnabled(enabled)
        self.ui.checkBox_file.setEnabled(enabled)
        self.ui.lineEdit_path.setEnabled(enabled)
        self.ui.pushButton_choose_path.setEnabled(enabled)
        self.ui.comboBox_source.setEnabled(enabled)
        self.ui.pushButton_pause.setEnabled(not enabled)

    def _configure_plot(self):
        """
        Configures specific elements of the PyQtGraph plots.
        :return:
        """
        self.ui.plt.setAutoFillBackground(False)
        self.ui.plt.setStyleSheet("border: 0px;")
        self.ui.plt.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ui.plt.setFrameShadow(QtWidgets.QFrame.Plain)
        self.ui.plt.setLineWidth(0)
        self.ui.plt.setBackground(background=None)
        self.ui.plt.setAntialiasing(True)

    def _configure_timers(self):
        """
        Configures specific elements of the QTimers.
        :return:
        """
        self._timer_plot = QtCore.QTimer(self)
        self._timer_table = QtCore.QTimer(self)
        self._timer_plot.timeout.connect(self._update_plot)
        self._timer_plot.setInterval(SysConfig.plot_update_ms)
        self._timer_table.timeout.connect(self._update_table_view)
        self._timer_table.setInterval(SysConfig.table_update_ms)
    def _update_csv_path(self, checked):
        if checked and not len(self.ui.lineEdit_path.text()):
            default_full_path = str("{}/{}{}".format(SysConfig.app_export_path, strftime(SysConfig.csv_filename, gmtime()), SysConfig.csv_extension))
            self.ui.lineEdit_path.setText(default_full_path)
    def _choose_csv_path(self):
        default_full_path = str("{}/{}{}".format(SysConfig.app_export_path, strftime(SysConfig.csv_filename, gmtime()), SysConfig.csv_extension))
        fileName, filter = QFileDialog.getSaveFileName(self, "Save F:xile",
                                            default_full_path,
                                            "CSV (*.csv)")
        if len(fileName): 
            self.ui.lineEdit_path.setText(fileName)
    def _update_channel_param_view(self, channel):
        self.ui.linee_raw.clear()
        self.ui.linee_smooth.clear()
        self.ui.linee_baseline.clear()
        self.ui.linee_diff_max.clear()
        self.ui.linee_diff_ratio.clear()
        #load current param
        if TpConfig.Current.param["slope"][channel] != -1:
            self.ui.comb_slope.setCurrentIndex(TpConfig.Current.param["slope"][channel])
        else:
            self.ui.comb_slope.setCurrentIndex(TpConfig.MeasChannel.slope["dflt"])
        if TpConfig.Current.param["opt"][channel] != -1:
            self.ui.comb_opt.setCurrentIndex(TpConfig.Current.param["opt"][channel])
        else:
            self.ui.comb_opt.setCurrentIndex(TpConfig.MeasChannel.opt["dflt"])
        if TpConfig.Current.param["threshold_ratio"][channel] != -1:
            self.ui.spin_threshold_ratio.setValue(TpConfig.Current.param["threshold_ratio"][channel])
        else:
            self.ui.spin_threshold_ratio.setValue(TpConfig.JudgeChannel.threshold_ratio["dflt"])

        self._update_plot_view_diff(False)
        self._update_plot_view_diff(self.ui.checkb_plot_diff.isChecked())
    def _update_jitter_filter(self):
        if self.ui.comb_fmode.currentIndex() == 7:
            self.ui.comb_jitter_step.setEnabled(True)
        else:
            self.ui.comb_jitter_step.setEnabled(False)

    def _update_table_view(self):
        trigger_config_lists = [] #also add configs feedback here
        raw_value_str = ""
        update_ui_param = 0
        while True:
            trigger = self.worker.get_trigger_config_buffer()
            if trigger == []:
                break
            trigger_config_lists.append(trigger)
        if len(trigger_config_lists):
            for tg in trigger_config_lists:
                if tg[0] == SysConfig.trigger_format[0]:
                    channel = int(tg[SysConfig.trigger_channel_index])
                    time = int(tg[SysConfig.trigger_time_index])
                    sms_value = tg[SysConfig.trigger_value_index]
                        # Add three infinite lines with labels
                    for i in range(len(tg)-1):
                        itm=QTableWidgetItem('{}'.format(tg[i+1]))
                        self.ui.tableWidget.setItem(self._count_triggers, i, itm)
                        self.ui.tableWidget.scrollToItem(itm)
                    if self.ui.checkBox_plot_trigger.isChecked() and self._timer_plot.isActive() and (self._channel_choosed_mask & (0x0001<< channel)):
                        if tg[SysConfig.trigger_active_index] == '1':
                            plt_infi = pg.InfiniteLine(pos=time, movable=False, angle=90, pen='#FF6C33', label='Active='+sms_value, 
                                labelOpts={'position':0.8, 'color': '#FF6C33', 'movable': True})
                            self._plt_infi.append([time, channel, plt_infi])
                            self._plt[channel].addItem(plt_infi)
                            if self.ui.checkb_plot_diff.isChecked():
                                plt_infi2 = pg.InfiniteLine(pos=time, movable=False, angle=90, pen='#FF6C33', label='Active'+sms_value, 
                                                            labelOpts={'position':0.8, 'color': '#FF6C33', 'movable': True})
                                self._plt[SysConfig.diff_channel].addItem(plt_infi2)
                                self._plt_infi.append([time, SysConfig.diff_channel, plt_infi2])
                        if tg[SysConfig.trigger_inactive_index] == '1':
                            plt_infi = pg.InfiniteLine(pos=time, movable=False, angle=90, pen='#D733FF', label='InActive='+sms_value, 
                                        labelOpts={'position':0.6, 'color': '#D733FF', 'movable': True})
                            self._plt[channel].addItem(plt_infi)
                            self._plt_infi.append([time, channel, plt_infi])
                            if self.ui.checkb_plot_diff.isChecked():
                                plt_infi2 = pg.InfiniteLine(pos=time, movable=False, angle=90, pen='#D733FF', label='InActive'+sms_value, 
                                        labelOpts={'position':0.6, 'color': '#D733FF', 'movable': True})
                                self._plt[SysConfig.diff_channel].addItem(plt_infi2)
                                self._plt_infi.append([time, SysConfig.diff_channel, plt_infi2])
                    self._count_triggers+=1
                elif tg[0] == SysConfig.config_format[0]:
                    update_ui_param = 1
                    channel = int(tg[SysConfig.config_channel_index])
                    if tg[SysConfig.config_type_index] == "int" or tg[SysConfig.config_type_index] == "uint":
                        if channel == -1:
                            TpConfig.Current.param[tg[SysConfig.config_key_index]] = int(tg[SysConfig.config_value_index])
                        else:
                            TpConfig.Current.param[tg[SysConfig.config_key_index]][channel] = int(tg[SysConfig.config_value_index])
                    elif tg[SysConfig.config_type_index] == "hex":
                        if channel == -1:
                            TpConfig.Current.param[tg[SysConfig.config_key_index]] = int(tg[SysConfig.config_value_index], 16)
                        else:
                            TpConfig.Current.param[tg[SysConfig.config_key_index]][channel] = int(tg[SysConfig.config_value_index], 16)
                    elif tg[SysConfig.config_type_index] == "float":
                        if channel == -1:
                            TpConfig.Current.param[tg[SysConfig.config_key_index]] = float(tg[SysConfig.config_value_index])
                        else:
                            TpConfig.Current.param[tg[SysConfig.config_key_index]][channel] = float(tg[SysConfig.config_value_index])
                    elif tg[SysConfig.config_type_index] == "str":
                        if channel == -1:
                            TpConfig.Current.param[tg[SysConfig.config_key_index]] = str(tg[SysConfig.config_value_index])
                        else:
                            TpConfig.Current.param[tg[SysConfig.config_key_index]][channel] = str(tg[SysConfig.config_value_index])
                    Log.d(TAG, "{} {}:{} ({})".format(channel, tg[SysConfig.config_key_index],tg[SysConfig.config_value_index], tg[SysConfig.config_type_index]))
        if update_ui_param:
            self._updata_current_options()
        while True:
            value = self.worker.get_raw_buffer()
            if value == []:
                break
            raw_value_str += value[0].decode('latin-1', 'replace')
        if len(raw_value_str):
            self.ui.tab_log_rcv.appendPlainText(raw_value_str)

    def _update_plot_view_diff(self, check):
        self._update_plot_view(SysConfig.diff_channel, check)
    def _update_plot_pause(self):
        if self._timer_ref == 0:
            return
        if self._timer_plot_pause == 0:
            self._timer_plot.stop()
            Log.i(TAG, "Plot timmer pause\n")
            self._timer_plot_pause = 1
            self.ui.pushButton_plot_ctrl.setText("Resume")
            self._enable_plot_chan(0x7FFE,False)
        else:
            self._timer_plot.start()
            Log.i(TAG, "Plot timmer resume\n")
            self._timer_plot_pause = 0
            self.ui.pushButton_plot_ctrl.setText("Pause")
            self._enable_plot_chan(0x7FFE,True)
    def _update_plot_view(self, channel, check):
        if check == True:
            if self._plt[channel] != None:
                return
            self._plt[channel] = self.ui.plt.addPlot(row=channel, col=0)
            if channel == SysConfig.diff_channel:
                self._plt[channel].setLabel('left', "Diff CH{}".format(self.ui.comb_ch.currentIndex()))
            else:
                self._plt[channel].setLabel('left', "CH{}".format(channel))
            self._plt[channel].setLabel('bottom', SysConfig.plot_xlabel_title, SysConfig.plot_xlabel_unit)
            self._plt[channel].showGrid(x=True,y=True,alpha=0.5)
            self._plt[channel].addLegend()

            for idx in range(0, SysConfig.plot_max_lines):
                if channel == SysConfig.diff_channel:
                    self._plt_curve[channel][2] = self._plt[channel].plot(pen='#E53816', name="diff")
                    return
                elif channel <= SysConfig.plot_max_channels:
                    self._plt_curve[channel][idx] = self._plt[channel].plot(pen=SysConfig.plot_colors[idx], name=SysConfig.plot_legends[idx])
            self._timer_ref = self._timer_ref + 1
            self._channel_choosed_mask |= 0x0001 << channel
            self._command_enable_output()
            if self._timer_ref == 1:
                self._timer_plot.start()
                Log.i(TAG, "Plot timmer start\n")
        else:
            if self._plt[channel] == None:
                return
            self._plt[channel].clear()
            self.ui.plt.removeItem(self._plt[channel])
            self._plt[channel] = None
            if channel == SysConfig.diff_channel:
                return
            self._timer_ref = self._timer_ref - 1
            self._channel_choosed_mask &= ((~(0x0001 << channel)) & 0x7FFE)
            self._command_enable_output()
            if self._timer_ref == 0:
                self._timer_plot.stop()
                Log.i(TAG, "Plot timmer stop\n")
    def _diable_command(self, disable):
        self._command_disabled = disable
    def _command_config_measure_channel(self):
        if self.worker is None or self._command_disabled:
            return
        arg0 = self.ui.comb_ch.currentIndex()
        arg1 = self.ui.comb_slope.currentIndex()
        arg2 = self.ui.comb_opt.currentIndex()
        command = TpCommand.cmd_meas_channel(arg0, arg1, arg2)
        self.worker.send_command(command)
    def _command_config_judge_channel(self):
        if self.worker is None or self._command_disabled:
            return
        arg0 = self.ui.comb_ch.currentIndex()
        #TODO: enable_handler BY DEFAULT
        arg1 = 1
        #if using .value(), precision will cause problem, 16.9999 will be round down
        arg2 = float(self.ui.spin_threshold_ratio.text())
        command = TpCommand.cmd_judge_channel(arg0, arg1, arg2)
        self.worker.send_command(command)
    def _command_edit_send(self):
        if self.worker is None or self._command_disabled:
            return
        command = self.ui.tab_log_snd.toPlainText()
        self.worker.send_command(command)
    def _command_config_measure_gloabl(self):
        if self.worker is None or self._command_disabled:
            return
        arg0 = self.ui.spin_sleep_cycle.value()
        arg1 = self.ui.spin_meas_times.value()
        arg2 = self.ui.comb_refh.currentIndex()
        arg3 = self.ui.comb_refl.currentIndex()
        arg4 = self.ui.comb_atten.currentIndex()
        arg5 = self.ui.comb_pad_conn.currentIndex()
        arg6 = 1 if self.ui.checkb_enable_denoise.isChecked() else 0
        arg7 = self.ui.comb_grade.currentIndex()
        arg8 = self.ui.comb_cap_level.currentIndex()
        command = TpCommand.cmd_meas_global(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8)
        self.worker.send_command(command)
    def _command_config_judge_gloabl(self):
        if self.worker is None or self._command_disabled:
            return
        arg0 = 1 if self.ui.checkb_enable_filter.isChecked() else 0
        arg1 = self.ui.comb_fmode.currentIndex()
        arg2 = self.ui.comb_debounce_cnt.currentIndex()
        arg3 = self.ui.comb_noise_thr.currentIndex()
        arg4 = self.ui.comb_jitter_step.currentIndex()
        arg5 = self.ui.comb_smh_lvl.currentIndex()
        arg7 = 0
        arg6 = 1 if self.ui.checkb_enable_enable_interrupt.isChecked() else 0
        arg7 |= self.ui.checkb_interrupt_mask_active.isChecked() << 1
        arg7 |= self.ui.checkb_interrupt_mask_inactive.isChecked() << 2
        arg7 |= self.ui.checkb_interrupt_mask_scandone.isChecked() << 3
        arg7 |= self.ui.checkb_interrupt_mask_timeout.isChecked() << 4
        command = TpCommand.cmd_judge_global(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7)
        self.worker.send_command(command)
    def _command_enter_deepsleep(self):
        if self.worker is None or self._command_disabled:
            return
        fix_threshold = 0
        if self.ui.checkb_fix_threshold.isChecked():
                fix_threshold = self.ui.spin_fix_threshold_value.value()
        command = TpCommand.cmd_enter_deep_sleep(0x0001 << self.ui.combob_ch_sleep.currentIndex(),\
                    self.ui.spin_sleep_cycle_sleep.value(),\
                    self.ui.spin_meas_times_sleep.value(),\
                    float(self.ui.spin_threshold_ratio_sleep.text()),\
                    fix_threshold)
        self.worker.send_command(command)
        if self._touch_in_sleep == 0:
            self._touch_in_sleep = 1
    def _command_enter_lightsleep(self):
        if self.worker is None or self._command_disabled:
            return
        command = TpCommand.cmd_enter_light_sleep(0x0001 << self.ui.combob_ch_sleep.currentIndex())
        self.worker.send_command(command)
    def _command_reset_baseline(self):
        if self.worker is None or self._command_disabled:
            return
        command = TpCommand.cmd_reset_baseline(0x0001 << self.ui.comb_ch.currentIndex())
        self.worker.send_command(command)
    def _command_chip_restart(self):
        if self.worker is None or self._command_disabled:
            return
        command = TpCommand.cmd_chip_restart()
        Log.i(TAG, "restart chip\n")
        self.worker.send_command(command)
        sleep(SysConfig.chip_boot_time_s)
        self.worker.reset_buffers(self.ui.spin_samples.value())
        self._command_enable_output()
        Log.i(TAG, "restart chip done\n")
    def _command_enable_output(self):
        if self.worker is None or self._command_disabled:
            return
        if self._channel_choosed_mask & 0x7FFE != 0:
            speed_ms = 1000 // self.ui.spin_samples_freq.value()
            command = TpCommand.cmd_output_enable(speed_ms, self._channel_choosed_mask)
            self.worker.send_command(command)
        else:
            command = TpCommand.cmd_output_enable(-1)
            self.worker.send_command(command)
    def _configure_signals(self):
        """
        Configures the connections between signals and UI elements.
        :return:
        """
        self.ui.spin_threshold_ratio.textChanged.connect(self._command_config_judge_channel)
        self.ui.comb_slope.currentIndexChanged.connect(self._command_config_measure_channel)
        self.ui.comb_opt.currentIndexChanged.connect(self._command_config_measure_channel)
        self.ui.btn_lightsleep.clicked.connect(self._command_enter_lightsleep)
        self.ui.btn_deepsleep.clicked.connect(self._command_enter_deepsleep)
        self.ui.pushButton_chiprestart.clicked.connect(self._command_chip_restart)
        self.ui.btn_reset_baseline.clicked.connect(self._command_reset_baseline)
        self.ui.checkBox_file.toggled.connect(self._update_csv_path)
        self.ui.pushButton_clear.clicked.connect(self._clear_plot)
        self.ui.pushButton_choose_path.clicked.connect(self._choose_csv_path)
        self.ui.pushButton_start.clicked.connect(self.start)
        self.ui.pushButton_plot_ctrl.clicked.connect(self._update_plot_pause)
        self.ui.pushButton_pause.clicked.connect(self.stop)
        self.ui.spin_samples.valueChanged.connect(self._update_sample_size)
        self.ui.comboBox_source.activated.connect(self._source_changed)
        self.ui.checkb_plot_diff.toggled.connect(self._update_plot_view_diff)
        self.ui.buttonGroup.idToggled.connect(self._update_plot_view)
        self.ui.spin_sleep_cycle.textChanged.connect(self._command_config_measure_gloabl)
        self.ui.spin_meas_times.textChanged.connect(self._command_config_measure_gloabl)
        self.ui.comb_refh.currentIndexChanged.connect(self._command_config_measure_gloabl)
        self.ui.comb_refl.currentIndexChanged.connect(self._command_config_measure_gloabl)
        self.ui.comb_atten.currentIndexChanged.connect(self._command_config_measure_gloabl)
        self.ui.comb_pad_conn.currentIndexChanged.connect(self._command_config_measure_gloabl)
        self.ui.checkb_enable_denoise.toggled.connect(self._command_config_measure_gloabl)
        self.ui.comb_grade.currentIndexChanged.connect(self._command_config_measure_gloabl)
        self.ui.comb_cap_level.currentIndexChanged.connect(self._command_config_measure_gloabl)

        self.ui.checkb_enable_filter.toggled.connect(self._command_config_judge_gloabl)
        self.ui.comb_fmode.currentIndexChanged.connect(self._command_config_judge_gloabl)
        self.ui.comb_fmode.currentIndexChanged.connect(self._update_jitter_filter)
        self.ui.comb_debounce_cnt.currentIndexChanged.connect(self._command_config_judge_gloabl)
        self.ui.comb_noise_thr.currentIndexChanged.connect(self._command_config_judge_gloabl)
        self.ui.comb_jitter_step.currentIndexChanged.connect(self._command_config_judge_gloabl)
        self.ui.comb_smh_lvl.currentIndexChanged.connect(self._command_config_judge_gloabl)
        self.ui.checkb_enable_enable_interrupt.toggled.connect(self._command_config_judge_gloabl)
        self.ui.checkb_interrupt_mask_active.toggled.connect(self._command_config_judge_gloabl)
        self.ui.checkb_interrupt_mask_inactive.toggled.connect(self._command_config_judge_gloabl)
        self.ui.checkb_interrupt_mask_scandone.toggled.connect(self._command_config_judge_gloabl)
        self.ui.checkb_interrupt_mask_timeout.toggled.connect(self._command_config_judge_gloabl)
        self.ui.comb_ch.currentIndexChanged.connect(self._update_channel_param_view)

        self.ui.checkb_enable_denoise.toggled['bool'].connect(self.ui.comb_grade.setEnabled) # type: ignore
        self.ui.checkb_enable_denoise.toggled['bool'].connect(self.ui.comb_cap_level.setEnabled) # type: ignore
        self.ui.checkb_enable_filter.toggled['bool'].connect(self.ui.comb_fmode.setEnabled) # type: ignore
        self.ui.checkb_enable_filter.toggled['bool'].connect(self.ui.comb_debounce_cnt.setEnabled) # type: ignore
        self.ui.checkb_enable_filter.toggled['bool'].connect(self.ui.comb_noise_thr.setEnabled) # type: ignore
        #self.ui.checkb_enable_filter.toggled['bool'].connect(self.ui.comb_jitter_step.setEnabled) # type: ignore
        self.ui.checkb_enable_filter.toggled['bool'].connect(self.ui.comb_smh_lvl.setEnabled) # type: ignore
        self.ui.checkb_enable_enable_interrupt.toggled['bool'].connect(self.ui.checkb_interrupt_mask_active.setEnabled) # type: ignore
        self.ui.checkb_enable_enable_interrupt.toggled['bool'].connect(self.ui.checkb_interrupt_mask_inactive.setEnabled) # type: ignore
        self.ui.checkb_enable_enable_interrupt.toggled['bool'].connect(self.ui.checkb_interrupt_mask_scandone.setEnabled) # type: ignore
        self.ui.checkb_enable_enable_interrupt.toggled['bool'].connect(self.ui.checkb_interrupt_mask_timeout.setEnabled) # type: ignore
        self.ui.checkb_fix_threshold.toggled['bool'].connect(self.ui.spin_fix_threshold_value.setEnabled) # type: ignore
        self.ui.checkb_fix_threshold.toggled['bool'].connect(self.ui.spin_threshold_ratio_sleep.setDisabled) # type: ignore
        self.ui.btn_clear_rcv.clicked.connect(self.ui.tab_log_rcv.clear)
        self.ui.btn_clear_snd.clicked.connect(self.ui.tab_log_snd.clear)
        self.ui.btn_log_sed.clicked.connect(self._command_edit_send)

    def _clear_plot(self):
        self._update_sample_size()
        self._command_enable_output()
    def _update_sample_size(self):
        """
        Updates the sample size of the plot.
        This function is connected to the valueChanged signal of the sample Spin Box.
        :return:
        """
        if self.worker is not None:
            Log.i(TAG, "Changing sample size")
            self.worker.reset_buffers(self.ui.spin_samples.value())
    def _updata_current_options(self):
        self._diable_command(True)
        if TpConfig.Current.param["sample_freq"] != -1:
            self.ui.spin_samples_freq.setValue(TpConfig.Current.param["sample_freq"])
        if TpConfig.Current.param["sleep_cycle"] != -1:
            self.ui.spin_sleep_cycle.setValue(TpConfig.Current.param["sleep_cycle"])
        if TpConfig.Current.param["meas_times"] != -1:
            self.ui.spin_meas_times.setValue(TpConfig.Current.param["meas_times"])
        if TpConfig.Current.param["pad_conn"] != -1:
            self.ui.comb_pad_conn.setCurrentIndex(TpConfig.Current.param["pad_conn"])
        if TpConfig.Current.param["refh"] != -1:
            self.ui.comb_refh.setCurrentIndex(TpConfig.Current.param["refh"])
        if TpConfig.Current.param["refl"] != -1:
            self.ui.comb_refl.setCurrentIndex(TpConfig.Current.param["refl"])
        if TpConfig.Current.param["atten"] != -1:
            self.ui.comb_atten.setCurrentIndex(TpConfig.Current.param["atten"])

        if TpConfig.Current.param["enable_denoise"] != -1:
            self.ui.checkb_enable_denoise.setCheckState(Qt.Checked if TpConfig.Current.param["enable_denoise"]==1 else Qt.Unchecked)
        if TpConfig.Current.param["grade"] != -1:
            self.ui.comb_grade.setCurrentIndex(TpConfig.Current.param["grade"])
        if TpConfig.Current.param["cap_level"] != -1:
            self.ui.comb_cap_level.setCurrentIndex(TpConfig.Current.param["cap_level"])
        if TpConfig.Current.param["enable_filter"] != -1:
            self.ui.checkb_enable_filter.setCheckState(Qt.Checked if TpConfig.Current.param["enable_filter"]==1 else Qt.Unchecked)
        if TpConfig.Current.param["mode"] != -1:
            self.ui.comb_fmode.setCurrentIndex(TpConfig.Current.param["mode"])
        if TpConfig.Current.param["debounce_cnt"] != -1:
            self.ui.comb_debounce_cnt.setCurrentIndex(TpConfig.Current.param["debounce_cnt"])
        if TpConfig.Current.param["noise_thr"] != -1:
            self.ui.comb_noise_thr.setCurrentIndex(TpConfig.Current.param["noise_thr"])
        if TpConfig.Current.param["jitter_step"] != -1:
            self.ui.comb_jitter_step.setCurrentIndex(TpConfig.Current.param["jitter_step"])
        if TpConfig.Current.param["smh_lvl"] != -1:
            self.ui.comb_smh_lvl.setCurrentIndex(TpConfig.Current.param["smh_lvl"])
        if TpConfig.Current.param["enable_interrupt"] != -1:
            self.ui.checkb_enable_enable_interrupt.setCheckState(Qt.Checked if TpConfig.Current.param["enable_interrupt"]==1 else Qt.Unchecked)
        focus_channel = self.ui.comb_ch.currentIndex()
        if TpConfig.Current.param["threshold_ratio"][focus_channel] != -1:
            self.ui.spin_threshold_ratio.setValue(TpConfig.Current.param["threshold_ratio"][focus_channel])
        if TpConfig.Current.param["slope"][focus_channel] != -1:
            self.ui.comb_slope.setCurrentIndex(TpConfig.Current.param["slope"][focus_channel])
        if TpConfig.Current.param["opt"][focus_channel] != -1:
            self.ui.comb_opt.setCurrentIndex(TpConfig.Current.param["opt"][focus_channel])
        focus_channel = self.ui.combob_ch_sleep.currentIndex()
        if TpConfig.Current.param["smooth_deepsleep"][focus_channel] != -1:
            self.ui.linee_value_sleep.setText("{}".format(TpConfig.Current.param["smooth_deepsleep"][focus_channel]))
            if self._touch_in_sleep == 1:
                self._touch_in_sleep = 2
        if TpConfig.Current.param["baseline_deepsleep"][focus_channel] != -1:
            self.ui.linee_sleep_baseline.setText("{}".format(TpConfig.Current.param["baseline_deepsleep"][focus_channel]))
        if TpConfig.Current.param["smooth_deepsleep_out"][focus_channel] != -1:
            self.ui.linee_value_wakeup.setText("{}".format(TpConfig.Current.param["smooth_deepsleep_out"][focus_channel]))
        if TpConfig.Current.param["diff_deepsleep_out"][focus_channel] != -1:
            self.ui.linee_value_diff.setText("{}".format(TpConfig.Current.param["diff_deepsleep_out"][focus_channel]))
            if self._touch_in_sleep == 2:
                self._touch_in_sleep = 0
                sleep(SysConfig.chip_boot_time_s)
                self._diable_command(False)
                self._clear_plot()
        self._diable_command(False)
    def _reset_default_options(self):
        self.ui.checkBox_plot_trigger.setCheckState(Qt.Checked)
        self.ui.checkb_interrupt_mask_active.setCheckState(Qt.Checked)
        self.ui.checkb_interrupt_mask_inactive.setCheckState(Qt.Checked)
        self.ui.spin_samples_freq.setValue(TpConfig.Touch.sample_freq["dflt"])
        self.ui.spin_sleep_cycle.setValue(TpConfig.MeasGlobal.sleep_cycle["dflt"])
        self.ui.spin_meas_times.setValue(TpConfig.MeasGlobal.meas_times["dflt"])
        self.ui.spin_threshold_ratio.setValue(TpConfig.JudgeChannel.threshold_ratio["dflt"])
        self.ui.comb_ch.setCurrentIndex(TpConfig.Touch.channels["dflt"])
        self.ui.combob_ch_sleep.setCurrentIndex(TpConfig.Touch.channels["dflt"])
        self.ui.comb_pad_conn.setCurrentIndex(TpConfig.MeasGlobal.pad_conn["dflt"])
        self.ui.comb_refh.setCurrentIndex(TpConfig.MeasGlobal.refh["dflt"])
        self.ui.comb_refl.setCurrentIndex(TpConfig.MeasGlobal.refl["dflt"])
        self.ui.comb_atten.setCurrentIndex(TpConfig.MeasGlobal.atten["dflt"])

        self.ui.spin_sleep_cycle_sleep.setValue(TpConfig.SleepParam.sleep_cycle["dflt"])
        self.ui.spin_meas_times_sleep.setValue(TpConfig.SleepParam.meas_times["dflt"])
        self.ui.spin_threshold_ratio_sleep.setValue(TpConfig.SleepParam.threshold_ratio["dflt"])
        self.ui.spin_fix_threshold_value.setValue(TpConfig.SleepParam.threshold_value["dflt"])
        #warkaround to emit state signal
        self.ui.checkb_fix_threshold.setCheckState(Qt.Checked if TpConfig.SleepParam.enable_fixed_threshold["dflt"] == 1 else Qt.Unchecked)
        self.ui.checkb_enable_denoise.setCheckState(Qt.Checked if TpConfig.MeasGlobal.enable_denoise["dflt"] == 1 else Qt.Unchecked)
        self.ui.comb_grade.setCurrentIndex(TpConfig.MeasGlobal.grade["dflt"])
        self.ui.comb_cap_level.setCurrentIndex(TpConfig.MeasGlobal.cap_level["dflt"])
        self.ui.comb_slope.setCurrentIndex(TpConfig.MeasChannel.slope["dflt"])
        self.ui.comb_opt.setCurrentIndex(TpConfig.MeasChannel.opt["dflt"])
        self.ui.comb_fmode.setCurrentIndex(TpConfig.JudgeGlobal.mode["dflt"])
        self.ui.comb_debounce_cnt.setCurrentIndex(TpConfig.JudgeGlobal.debounce_cnt["dflt"])
        self.ui.comb_noise_thr.setCurrentIndex(TpConfig.JudgeGlobal.noise_thr["dflt"])
        self.ui.comb_jitter_step.setCurrentIndex(TpConfig.JudgeGlobal.jitter_step["dflt"])
        self.ui.comb_smh_lvl.setCurrentIndex(TpConfig.JudgeGlobal.smh_lvl["dflt"])
        self.ui.checkb_enable_filter.setCheckState(Qt.Checked if TpConfig.JudgeGlobal.enable_filter["dflt"]==1 else Qt.Unchecked)
        self.ui.checkb_enable_enable_interrupt.setCheckState(Qt.Checked if TpConfig.JudgeGlobal.enable_interrupt["dflt"]==1 else Qt.Unchecked)

    def _update_options(self):
        self.ui.spin_samples_freq.setMinimum(TpConfig.Touch.sample_freq["min"])
        self.ui.spin_samples_freq.setMaximum(TpConfig.Touch.sample_freq["max"])
        self.ui.spin_sleep_cycle.setMinimum(TpConfig.MeasGlobal.sleep_cycle["min"])
        self.ui.spin_sleep_cycle.setMaximum(TpConfig.MeasGlobal.sleep_cycle["max"])
        self.ui.spin_meas_times.setMinimum(TpConfig.MeasGlobal.meas_times["min"])
        self.ui.spin_meas_times.setMaximum(TpConfig.MeasGlobal.meas_times["max"])
        self.ui.spin_threshold_ratio.setMinimum(TpConfig.JudgeChannel.threshold_ratio["min"])
        self.ui.spin_threshold_ratio.setMaximum(TpConfig.JudgeChannel.threshold_ratio["max"])
        self.ui.spin_fix_threshold_value.setMinimum(TpConfig.SleepParam.threshold_value["min"])
        self.ui.spin_fix_threshold_value.setMaximum(TpConfig.SleepParam.threshold_value["max"])
        self.ui.spin_sleep_cycle_sleep.setMinimum(TpConfig.SleepParam.sleep_cycle["min"])
        self.ui.spin_sleep_cycle_sleep.setMaximum(TpConfig.SleepParam.sleep_cycle["max"])
        self.ui.spin_meas_times_sleep.setMinimum(TpConfig.SleepParam.meas_times["min"])
        self.ui.spin_meas_times_sleep.setMaximum(TpConfig.SleepParam.meas_times["max"])
        self.ui.spin_threshold_ratio_sleep.setMinimum(TpConfig.SleepParam.threshold_ratio["min"])
        self.ui.spin_threshold_ratio_sleep.setMaximum(TpConfig.SleepParam.threshold_ratio["max"])
        self.ui.spin_threshold_ratio_sleep.setMinimum(TpConfig.SleepParam.threshold_ratio["min"])
        self.ui.spin_threshold_ratio_sleep.setMaximum(TpConfig.SleepParam.threshold_ratio["max"])
        self.ui.spin_threshold_ratio.setDecimals(3)
        self.ui.spin_threshold_ratio.setSingleStep(0.001)
        self.ui.spin_threshold_ratio_sleep.setDecimals(3)
        self.ui.spin_threshold_ratio_sleep.setSingleStep(0.001)
        self.ui.spin_fix_threshold_value.setSingleStep(1)
        for i in range(20):
            #Touch 
            if i in TpConfig.Touch.channels:
                self.ui.comb_ch.insertItem(i, TpConfig.Touch.channels[i])
            if i in TpConfig.Touch.channels:
                self.ui.combob_ch_sleep.insertItem(i, TpConfig.Touch.channels[i])
            #Measure global
            if i in TpConfig.MeasGlobal.pad_conn:
                self.ui.comb_pad_conn.insertItem(i, TpConfig.MeasGlobal.pad_conn[i])
            if i in TpConfig.MeasGlobal.refh:
                self.ui.comb_refh.insertItem(i, TpConfig.MeasGlobal.refh[i])
            if i in TpConfig.MeasGlobal.refl:
                self.ui.comb_refl.insertItem(i, TpConfig.MeasGlobal.refl[i])
            if i in TpConfig.MeasGlobal.atten:
                self.ui.comb_atten.insertItem(i, TpConfig.MeasGlobal.atten[i])
            if i in TpConfig.MeasGlobal.grade:
                self.ui.comb_grade.insertItem(i, TpConfig.MeasGlobal.grade[i])
            if i in TpConfig.MeasGlobal.cap_level:
                self.ui.comb_cap_level.insertItem(i, TpConfig.MeasGlobal.cap_level[i])
            #measure channel
            if i in TpConfig.MeasChannel.slope:
                self.ui.comb_slope.insertItem(i, TpConfig.MeasChannel.slope[i])
            if i in TpConfig.MeasChannel.opt:
                self.ui.comb_opt.insertItem(i, TpConfig.MeasChannel.opt[i])
            #judge global
            if i in TpConfig.JudgeGlobal.mode:
                self.ui.comb_fmode.insertItem(i, TpConfig.JudgeGlobal.mode[i])
            if i in TpConfig.JudgeGlobal.debounce_cnt:
                self.ui.comb_debounce_cnt.insertItem(i, TpConfig.JudgeGlobal.debounce_cnt[i])
            if i in TpConfig.JudgeGlobal.noise_thr:
                self.ui.comb_noise_thr.insertItem(i, TpConfig.JudgeGlobal.noise_thr[i])
            if i in TpConfig.JudgeGlobal.jitter_step:
                self.ui.comb_jitter_step.insertItem(i, TpConfig.JudgeGlobal.jitter_step[i])
            if i in TpConfig.JudgeGlobal.smh_lvl:
                self.ui.comb_smh_lvl.insertItem(i, TpConfig.JudgeGlobal.smh_lvl[i])
        self._reset_default_options()
    def _update_plot(self):
        """
        Updates and redraws the graphics in the plot.
        This function us connected to the timeout signal of a QTimer.
        :return:
        """
        if self.worker is None:
            return
        # load data to time/data ringbuffer
        self.worker.consume_queue()
        # plot data
        for channel in range(0, SysConfig.plot_max_channels + 3):
            if self._plt[channel] != None:
                raw,smooth,base = 0,0,0
                for idx in range(0, SysConfig.plot_max_lines):
                    x,y = None,None
                    if idx == 2 and channel == SysConfig.diff_channel and self.ui.checkb_plot_diff.isChecked():
                        focus_channel = self.ui.comb_ch.currentIndex()
                        x=self.worker.get_time_buffer(focus_channel)
                        y_smooth=self.worker.get_values_buffer(focus_channel, 1)
                        y_base=self.worker.get_values_buffer(focus_channel, 2)
                        if y_smooth != [] and y_base != []:
                            y = y_smooth - y_base
                            if y_base[0] != 0:
                                self._diff_max[focus_channel] = np.max(y)
                                self._diff_rate[focus_channel] = np.max(y) / y_base[0]
                            else:
                                self._diff_max[focus_channel] = 0
                                self._diff_rate[focus_channel] = 0
                        else:
                            continue  
                    elif channel <= SysConfig.plot_max_channels:
                        x=self.worker.get_time_buffer(channel)
                        y=self.worker.get_values_buffer(channel, idx)
                    else:
                        continue
                    if x.any() and y.any():
                        for i in range(14):
                            if self._plt_infi != [] and (x[len(x)-1] > self._plt_infi[0][0] or x[0] < self._plt_infi[0][0]):
                                self._plt[self._plt_infi[0][1]].removeItem(self._plt_infi[0][2])
                                self._plt_infi.pop(0)
                            else:
                                break
                        self._plt_curve[channel][idx].setData(x=x, y=y)
                        #calculate smooth data params
                        if channel == self.ui.comb_ch.currentIndex() and y[0] != 0:
                            #update 5 times each second
                            if self._diff_update_count <= SysConfig.param_update_ms:
                                self._diff_update_count += (1000 // self.ui.spin_samples_freq.value())
                                continue
                            else:
                                self._diff_update_count = 0
                            if idx == 0:
                                raw = y[0]
                                self.ui.linee_raw.setText('{:.0f}'.format(raw))
                                continue
                            elif idx == 1:
                                smooth = y[0]
                                self.ui.linee_smooth.setText('{:.0f}'.format(smooth))
                            elif idx == 2:
                                base = y[0]
                                self.ui.linee_baseline.setText('{:.0f}'.format(base))
                                continue
                            self.ui.linee_diff_max.setText('{:.2f}'.format(self._diff_max[channel]))
                            self.ui.linee_diff_ratio.setText('{:.3f}'.format(self._diff_rate[channel]))

    def _source_changed(self):
        """
        Updates the source and depending boxes on change.
        This function is connected to the indexValueChanged signal of the Source ComboBox.
        :return:
        """
        Log.i(TAG, "Scanning source {}".format(self._get_source().name))
        # clear boxes before adding new
        self.ui.comboBox_port.clear()
        self.ui.comboBox_portspd.clear()

        source = self._get_source()
        ports = Worker.get_source_ports(source)
        speeds = Worker.get_source_speeds(source)

        if ports is not None:
            self.ui.comboBox_port.addItems(ports)
        if speeds is not None:
            self.ui.comboBox_portspd.addItems(speeds)
        if self._get_source() == SourceType.serial:
            self.ui.comboBox_portspd.setCurrentIndex(len(speeds) - 1)

    def _get_source(self):
        """
        Gets the current source type.
        :return: Current Source type.
        :rtype: SourceType.
        """
        return SourceType(self.ui.comboBox_source.currentIndex())
