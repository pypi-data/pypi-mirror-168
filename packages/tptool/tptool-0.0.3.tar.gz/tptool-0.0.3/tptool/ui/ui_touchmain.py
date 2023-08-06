# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'touchmain.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from pyqtgraph import GraphicsLayoutWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1230, 960)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setKerning(True)
        self.groupBox.setFont(font)
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.checkBox_12 = QCheckBox(self.groupBox)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.setExclusive(False)
        self.buttonGroup.addButton(self.checkBox_12)
        self.checkBox_12.setObjectName(u"checkBox_12")
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(False)
        font1.setKerning(True)
        self.checkBox_12.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBox_12, 2, 3, 1, 1)

        self.checkBox_4 = QCheckBox(self.groupBox)
        self.buttonGroup.addButton(self.checkBox_4)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBox_4, 0, 3, 1, 1)

        self.checkBox_5 = QCheckBox(self.groupBox)
        self.buttonGroup.addButton(self.checkBox_5)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBox_5, 1, 0, 1, 1)

        self.checkBox_10 = QCheckBox(self.groupBox)
        self.buttonGroup.addButton(self.checkBox_10)
        self.checkBox_10.setObjectName(u"checkBox_10")
        self.checkBox_10.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBox_10, 2, 1, 1, 1)

        self.checkBox_13 = QCheckBox(self.groupBox)
        self.buttonGroup.addButton(self.checkBox_13)
        self.checkBox_13.setObjectName(u"checkBox_13")
        self.checkBox_13.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBox_13, 3, 0, 1, 1)

        self.checkBox_9 = QCheckBox(self.groupBox)
        self.buttonGroup.addButton(self.checkBox_9)
        self.checkBox_9.setObjectName(u"checkBox_9")
        self.checkBox_9.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBox_9, 2, 0, 1, 1)

        self.checkBox_14 = QCheckBox(self.groupBox)
        self.buttonGroup.addButton(self.checkBox_14)
        self.checkBox_14.setObjectName(u"checkBox_14")
        self.checkBox_14.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBox_14, 3, 1, 1, 1)

        self.checkBox_1 = QCheckBox(self.groupBox)
        self.buttonGroup.addButton(self.checkBox_1)
        self.checkBox_1.setObjectName(u"checkBox_1")
        self.checkBox_1.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBox_1, 0, 0, 1, 1)

        self.checkBox_6 = QCheckBox(self.groupBox)
        self.buttonGroup.addButton(self.checkBox_6)
        self.checkBox_6.setObjectName(u"checkBox_6")
        self.checkBox_6.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBox_6, 1, 1, 1, 1)

        self.checkBox_3 = QCheckBox(self.groupBox)
        self.buttonGroup.addButton(self.checkBox_3)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBox_3, 0, 2, 1, 1)

        self.checkBox_7 = QCheckBox(self.groupBox)
        self.buttonGroup.addButton(self.checkBox_7)
        self.checkBox_7.setObjectName(u"checkBox_7")
        self.checkBox_7.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBox_7, 1, 2, 1, 1)

        self.checkBox_8 = QCheckBox(self.groupBox)
        self.buttonGroup.addButton(self.checkBox_8)
        self.checkBox_8.setObjectName(u"checkBox_8")
        self.checkBox_8.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBox_8, 1, 3, 1, 1)

        self.checkBox_2 = QCheckBox(self.groupBox)
        self.buttonGroup.addButton(self.checkBox_2)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBox_2, 0, 1, 1, 1)

        self.checkBox_11 = QCheckBox(self.groupBox)
        self.buttonGroup.addButton(self.checkBox_11)
        self.checkBox_11.setObjectName(u"checkBox_11")
        self.checkBox_11.setFont(font1)

        self.gridLayout_2.addWidget(self.checkBox_11, 2, 2, 1, 1)

        self.pushButton_plot_ctrl = QPushButton(self.groupBox)
        self.pushButton_plot_ctrl.setObjectName(u"pushButton_plot_ctrl")

        self.gridLayout_2.addWidget(self.pushButton_plot_ctrl, 3, 3, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox, 2, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy1)
        self.groupBox_4.setFont(font)
        self.gridLayout_5 = QGridLayout(self.groupBox_4)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.checkBox_plot_trigger = QCheckBox(self.groupBox_4)
        self.checkBox_plot_trigger.setObjectName(u"checkBox_plot_trigger")
        self.checkBox_plot_trigger.setEnabled(True)
        self.checkBox_plot_trigger.setFont(font)

        self.gridLayout_5.addWidget(self.checkBox_plot_trigger, 1, 2, 1, 1)

        self.tableWidget = QTableWidget(self.groupBox_4)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy2)
        self.tableWidget.setFont(font1)

        self.gridLayout_5.addWidget(self.tableWidget, 2, 2, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_4, 1, 3, 2, 1)

        self.tab_main = QTabWidget(self.centralwidget)
        self.tab_main.setObjectName(u"tab_main")
        self.tab_main.setFont(font1)
        self.tab_main.setTabsClosable(False)
        self.tab_main.setMovable(False)
        self.tab_plot = QWidget()
        self.tab_plot.setObjectName(u"tab_plot")
        self.gridLayout_6 = QGridLayout(self.tab_plot)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.plt = GraphicsLayoutWidget(self.tab_plot)
        self.plt.setObjectName(u"plt")
        sizePolicy1.setHeightForWidth(self.plt.sizePolicy().hasHeightForWidth())
        self.plt.setSizePolicy(sizePolicy1)
        self.plt.setFont(font1)

        self.gridLayout_6.addWidget(self.plt, 0, 0, 1, 1)

        self.tab_main.addTab(self.tab_plot, "")
        self.tab_log = QWidget()
        self.tab_log.setObjectName(u"tab_log")
        self.gridLayout_7 = QGridLayout(self.tab_log)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.label_35 = QLabel(self.tab_log)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_7.addWidget(self.label_35, 2, 5, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.btn_clear_snd = QPushButton(self.tab_log)
        self.btn_clear_snd.setObjectName(u"btn_clear_snd")

        self.gridLayout_7.addWidget(self.btn_clear_snd, 2, 7, 1, 1)

        self.btn_log_sed = QPushButton(self.tab_log)
        self.btn_log_sed.setObjectName(u"btn_log_sed")

        self.gridLayout_7.addWidget(self.btn_log_sed, 2, 8, 1, 1)

        self.tab_log_snd = QTextEdit(self.tab_log)
        self.tab_log_snd.setObjectName(u"tab_log_snd")

        self.gridLayout_7.addWidget(self.tab_log_snd, 1, 0, 1, 9)

        self.tab_log_rcv = QPlainTextEdit(self.tab_log)
        self.tab_log_rcv.setObjectName(u"tab_log_rcv")
        self.tab_log_rcv.setReadOnly(True)

        self.gridLayout_7.addWidget(self.tab_log_rcv, 0, 0, 1, 9)

        self.label_33 = QLabel(self.tab_log)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_7.addWidget(self.label_33, 2, 2, 1, 1)

        self.label_snd_num = QLabel(self.tab_log)
        self.label_snd_num.setObjectName(u"label_snd_num")

        self.gridLayout_7.addWidget(self.label_snd_num, 2, 6, 1, 1)

        self.btn_clear_rcv = QPushButton(self.tab_log)
        self.btn_clear_rcv.setObjectName(u"btn_clear_rcv")

        self.gridLayout_7.addWidget(self.btn_clear_rcv, 2, 4, 1, 1)

        self.label_rev_num = QLabel(self.tab_log)
        self.label_rev_num.setObjectName(u"label_rev_num")

        self.gridLayout_7.addWidget(self.label_rev_num, 2, 3, 1, 1)

        self.gridLayout_7.setRowStretch(0, 8)
        self.gridLayout_7.setRowStretch(1, 2)
        self.tab_main.addTab(self.tab_log, "")

        self.gridLayout_4.addWidget(self.tab_main, 0, 0, 1, 4)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setPointSize(8)
        font2.setBold(True)
        self.groupBox_3.setFont(font2)
        self.gridLayout_9 = QGridLayout(self.groupBox_3)
        self.gridLayout_9.setSpacing(6)
        self.gridLayout_9.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.btn_reset_baseline_sleep = QPushButton(self.groupBox_3)
        self.btn_reset_baseline_sleep.setObjectName(u"btn_reset_baseline_sleep")
        self.btn_reset_baseline_sleep.setEnabled(False)
        font3 = QFont()
        font3.setPointSize(8)
        font3.setBold(False)
        self.btn_reset_baseline_sleep.setFont(font3)

        self.gridLayout_9.addWidget(self.btn_reset_baseline_sleep, 14, 0, 1, 1)

        self.label_37 = QLabel(self.groupBox_3)
        self.label_37.setObjectName(u"label_37")
        self.label_37.setFont(font3)

        self.gridLayout_9.addWidget(self.label_37, 11, 0, 1, 1)

        self.spin_sleep_cycle_sleep = QSpinBox(self.groupBox_3)
        self.spin_sleep_cycle_sleep.setObjectName(u"spin_sleep_cycle_sleep")
        self.spin_sleep_cycle_sleep.setFont(font3)

        self.gridLayout_9.addWidget(self.spin_sleep_cycle_sleep, 1, 1, 1, 1)

        self.label_32 = QLabel(self.groupBox_3)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font3)

        self.gridLayout_9.addWidget(self.label_32, 10, 0, 1, 1)

        self.label_29 = QLabel(self.groupBox_3)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setFont(font3)

        self.gridLayout_9.addWidget(self.label_29, 2, 0, 1, 1)

        self.spin_fix_threshold_value = QSpinBox(self.groupBox_3)
        self.spin_fix_threshold_value.setObjectName(u"spin_fix_threshold_value")
        self.spin_fix_threshold_value.setEnabled(False)

        self.gridLayout_9.addWidget(self.spin_fix_threshold_value, 5, 1, 1, 1)

        self.spin_threshold_ratio_sleep = QDoubleSpinBox(self.groupBox_3)
        self.spin_threshold_ratio_sleep.setObjectName(u"spin_threshold_ratio_sleep")
        self.spin_threshold_ratio_sleep.setFont(font3)

        self.gridLayout_9.addWidget(self.spin_threshold_ratio_sleep, 3, 1, 1, 1)

        self.label_34 = QLabel(self.groupBox_3)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setFont(font3)

        self.gridLayout_9.addWidget(self.label_34, 2, 1, 1, 1)

        self.spin_meas_times_sleep = QSpinBox(self.groupBox_3)
        self.spin_meas_times_sleep.setObjectName(u"spin_meas_times_sleep")
        self.spin_meas_times_sleep.setFont(font3)

        self.gridLayout_9.addWidget(self.spin_meas_times_sleep, 3, 0, 1, 1)

        self.linee_value_diff = QLineEdit(self.groupBox_3)
        self.linee_value_diff.setObjectName(u"linee_value_diff")
        self.linee_value_diff.setReadOnly(True)

        self.gridLayout_9.addWidget(self.linee_value_diff, 11, 1, 1, 1)

        self.checkb_wakeup_keep_thres = QCheckBox(self.groupBox_3)
        self.checkb_wakeup_keep_thres.setObjectName(u"checkb_wakeup_keep_thres")
        self.checkb_wakeup_keep_thres.setFont(font3)
        self.checkb_wakeup_keep_thres.setChecked(True)

        self.gridLayout_9.addWidget(self.checkb_wakeup_keep_thres, 14, 1, 1, 1)

        self.combob_ch_sleep = QComboBox(self.groupBox_3)
        self.combob_ch_sleep.setObjectName(u"combob_ch_sleep")
        self.combob_ch_sleep.setFont(font2)

        self.gridLayout_9.addWidget(self.combob_ch_sleep, 1, 0, 1, 1)

        self.checkb_fix_threshold = QCheckBox(self.groupBox_3)
        self.checkb_fix_threshold.setObjectName(u"checkb_fix_threshold")
        self.checkb_fix_threshold.setFont(font3)

        self.gridLayout_9.addWidget(self.checkb_fix_threshold, 4, 0, 1, 1)

        self.label_28 = QLabel(self.groupBox_3)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font3)

        self.gridLayout_9.addWidget(self.label_28, 0, 1, 1, 1)

        self.btn_deepsleep = QPushButton(self.groupBox_3)
        self.btn_deepsleep.setObjectName(u"btn_deepsleep")
        self.btn_deepsleep.setFont(font3)

        self.gridLayout_9.addWidget(self.btn_deepsleep, 15, 1, 1, 1)

        self.label_30 = QLabel(self.groupBox_3)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font3)

        self.gridLayout_9.addWidget(self.label_30, 0, 0, 1, 1)

        self.label_38 = QLabel(self.groupBox_3)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setFont(font3)

        self.gridLayout_9.addWidget(self.label_38, 9, 0, 1, 1)

        self.btn_lightsleep = QPushButton(self.groupBox_3)
        self.btn_lightsleep.setObjectName(u"btn_lightsleep")
        self.btn_lightsleep.setEnabled(False)
        self.btn_lightsleep.setFont(font3)

        self.gridLayout_9.addWidget(self.btn_lightsleep, 15, 0, 1, 1)

        self.label_36 = QLabel(self.groupBox_3)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setFont(font3)

        self.gridLayout_9.addWidget(self.label_36, 5, 0, 1, 1)

        self.linee_sleep_baseline = QLineEdit(self.groupBox_3)
        self.linee_sleep_baseline.setObjectName(u"linee_sleep_baseline")
        self.linee_sleep_baseline.setReadOnly(True)

        self.gridLayout_9.addWidget(self.linee_sleep_baseline, 9, 1, 1, 1)

        self.linee_value_sleep = QLineEdit(self.groupBox_3)
        self.linee_value_sleep.setObjectName(u"linee_value_sleep")
        self.linee_value_sleep.setReadOnly(True)

        self.gridLayout_9.addWidget(self.linee_value_sleep, 8, 1, 1, 1)

        self.linee_value_wakeup = QLineEdit(self.groupBox_3)
        self.linee_value_wakeup.setObjectName(u"linee_value_wakeup")
        self.linee_value_wakeup.setReadOnly(True)

        self.gridLayout_9.addWidget(self.linee_value_wakeup, 10, 1, 1, 1)

        self.label_31 = QLabel(self.groupBox_3)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font3)

        self.gridLayout_9.addWidget(self.label_31, 8, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_3, 1, 2, 2, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setFont(font)
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.gridLayout_3.addWidget(self.label_6, 3, 0, 1, 1)

        self.pushButton_start = QPushButton(self.groupBox_2)
        self.pushButton_start.setObjectName(u"pushButton_start")
        sizePolicy1.setHeightForWidth(self.pushButton_start.sizePolicy().hasHeightForWidth())
        self.pushButton_start.setSizePolicy(sizePolicy1)
        font4 = QFont()
        font4.setPointSize(9)
        font4.setBold(True)
        font4.setKerning(True)
        self.pushButton_start.setFont(font4)

        self.gridLayout_3.addWidget(self.pushButton_start, 5, 0, 1, 1)

        self.spin_samples_freq = QSpinBox(self.groupBox_2)
        self.spin_samples_freq.setObjectName(u"spin_samples_freq")
        self.spin_samples_freq.setFont(font)

        self.gridLayout_3.addWidget(self.spin_samples_freq, 3, 1, 1, 1)

        self.pushButton_pause = QPushButton(self.groupBox_2)
        self.pushButton_pause.setObjectName(u"pushButton_pause")
        sizePolicy1.setHeightForWidth(self.pushButton_pause.sizePolicy().hasHeightForWidth())
        self.pushButton_pause.setSizePolicy(sizePolicy1)
        self.pushButton_pause.setFont(font4)

        self.gridLayout_3.addWidget(self.pushButton_pause, 5, 1, 1, 1)

        self.comboBox_port = QComboBox(self.groupBox_2)
        self.comboBox_port.setObjectName(u"comboBox_port")
        sizePolicy1.setHeightForWidth(self.comboBox_port.sizePolicy().hasHeightForWidth())
        self.comboBox_port.setSizePolicy(sizePolicy1)
        self.comboBox_port.setFont(font1)

        self.gridLayout_3.addWidget(self.comboBox_port, 0, 1, 1, 1)

        self.comboBox_portspd = QComboBox(self.groupBox_2)
        self.comboBox_portspd.setObjectName(u"comboBox_portspd")
        self.comboBox_portspd.setFont(font1)

        self.gridLayout_3.addWidget(self.comboBox_portspd, 0, 2, 1, 1)

        self.spin_samples = QSpinBox(self.groupBox_2)
        self.spin_samples.setObjectName(u"spin_samples")
        self.spin_samples.setFont(font1)
        self.spin_samples.setMaximum(100000)

        self.gridLayout_3.addWidget(self.spin_samples, 2, 1, 1, 1)

        self.comboBox_source = QComboBox(self.groupBox_2)
        self.comboBox_source.setObjectName(u"comboBox_source")
        self.comboBox_source.setFont(font1)

        self.gridLayout_3.addWidget(self.comboBox_source, 0, 0, 1, 1)

        self.pushButton_choose_path = QPushButton(self.groupBox_2)
        self.pushButton_choose_path.setObjectName(u"pushButton_choose_path")
        sizePolicy.setHeightForWidth(self.pushButton_choose_path.sizePolicy().hasHeightForWidth())
        self.pushButton_choose_path.setSizePolicy(sizePolicy)
        self.pushButton_choose_path.setFont(font1)

        self.gridLayout_3.addWidget(self.pushButton_choose_path, 4, 2, 1, 1)

        self.checkBox_file = QCheckBox(self.groupBox_2)
        self.checkBox_file.setObjectName(u"checkBox_file")
        sizePolicy1.setHeightForWidth(self.checkBox_file.sizePolicy().hasHeightForWidth())
        self.checkBox_file.setSizePolicy(sizePolicy1)
        self.checkBox_file.setFont(font)

        self.gridLayout_3.addWidget(self.checkBox_file, 3, 2, 1, 1)

        self.lineEdit_path = QLineEdit(self.groupBox_2)
        self.lineEdit_path.setObjectName(u"lineEdit_path")
        sizePolicy1.setHeightForWidth(self.lineEdit_path.sizePolicy().hasHeightForWidth())
        self.lineEdit_path.setSizePolicy(sizePolicy1)
        self.lineEdit_path.setFont(font1)

        self.gridLayout_3.addWidget(self.lineEdit_path, 4, 0, 1, 2)

        self.pushButton_chiprestart = QPushButton(self.groupBox_2)
        self.pushButton_chiprestart.setObjectName(u"pushButton_chiprestart")
        self.pushButton_chiprestart.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_chiprestart.sizePolicy().hasHeightForWidth())
        self.pushButton_chiprestart.setSizePolicy(sizePolicy)
        font5 = QFont()
        font5.setPointSize(9)
        font5.setBold(False)
        font5.setItalic(False)
        font5.setUnderline(False)
        font5.setStrikeOut(False)
        font5.setKerning(True)
        self.pushButton_chiprestart.setFont(font5)

        self.gridLayout_3.addWidget(self.pushButton_chiprestart, 5, 2, 1, 1)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)

        self.gridLayout_3.addWidget(self.label_7, 2, 0, 1, 1)

        self.pushButton_clear = QPushButton(self.groupBox_2)
        self.pushButton_clear.setObjectName(u"pushButton_clear")

        self.gridLayout_3.addWidget(self.pushButton_clear, 2, 2, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.groupBox_6 = QGroupBox(self.centralwidget)
        self.groupBox_6.setObjectName(u"groupBox_6")
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setFont(font2)
        self.gridLayout_8 = QGridLayout(self.groupBox_6)
        self.gridLayout_8.setSpacing(6)
        self.gridLayout_8.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_17 = QLabel(self.groupBox_6)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font3)

        self.gridLayout_8.addWidget(self.label_17, 0, 0, 1, 1)

        self.comb_ch = QComboBox(self.groupBox_6)
        self.comb_ch.setObjectName(u"comb_ch")
        self.comb_ch.setFont(font1)

        self.gridLayout_8.addWidget(self.comb_ch, 0, 1, 1, 1)

        self.label_18 = QLabel(self.groupBox_6)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font3)

        self.gridLayout_8.addWidget(self.label_18, 0, 2, 1, 1)

        self.comb_slope = QComboBox(self.groupBox_6)
        self.comb_slope.setObjectName(u"comb_slope")
        self.comb_slope.setFont(font2)

        self.gridLayout_8.addWidget(self.comb_slope, 0, 3, 1, 1)

        self.label_19 = QLabel(self.groupBox_6)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font3)

        self.gridLayout_8.addWidget(self.label_19, 0, 4, 1, 1)

        self.comb_opt = QComboBox(self.groupBox_6)
        self.comb_opt.setObjectName(u"comb_opt")
        self.comb_opt.setFont(font2)

        self.gridLayout_8.addWidget(self.comb_opt, 0, 5, 1, 1)

        self.label_27 = QLabel(self.groupBox_6)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font3)

        self.gridLayout_8.addWidget(self.label_27, 1, 0, 1, 1)

        self.spin_threshold_ratio = QDoubleSpinBox(self.groupBox_6)
        self.spin_threshold_ratio.setObjectName(u"spin_threshold_ratio")
        self.spin_threshold_ratio.setFont(font3)

        self.gridLayout_8.addWidget(self.spin_threshold_ratio, 1, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox_6)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.gridLayout_8.addWidget(self.label_3, 1, 2, 1, 1)

        self.linee_diff_ratio = QLineEdit(self.groupBox_6)
        self.linee_diff_ratio.setObjectName(u"linee_diff_ratio")
        self.linee_diff_ratio.setFont(font1)
        self.linee_diff_ratio.setReadOnly(True)

        self.gridLayout_8.addWidget(self.linee_diff_ratio, 1, 3, 1, 1)

        self.label_2 = QLabel(self.groupBox_6)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)

        self.gridLayout_8.addWidget(self.label_2, 1, 4, 1, 1)

        self.linee_diff_max = QLineEdit(self.groupBox_6)
        self.linee_diff_max.setObjectName(u"linee_diff_max")
        self.linee_diff_max.setFont(font1)
        self.linee_diff_max.setReadOnly(True)

        self.gridLayout_8.addWidget(self.linee_diff_max, 1, 5, 1, 1)

        self.label_4 = QLabel(self.groupBox_6)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.gridLayout_8.addWidget(self.label_4, 2, 0, 1, 1)

        self.linee_raw = QLineEdit(self.groupBox_6)
        self.linee_raw.setObjectName(u"linee_raw")
        self.linee_raw.setFont(font1)
        self.linee_raw.setReadOnly(True)

        self.gridLayout_8.addWidget(self.linee_raw, 2, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox_6)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.gridLayout_8.addWidget(self.label_5, 2, 2, 1, 1)

        self.linee_smooth = QLineEdit(self.groupBox_6)
        self.linee_smooth.setObjectName(u"linee_smooth")
        self.linee_smooth.setFont(font1)
        self.linee_smooth.setReadOnly(True)

        self.gridLayout_8.addWidget(self.linee_smooth, 2, 3, 1, 1)

        self.label = QLabel(self.groupBox_6)
        self.label.setObjectName(u"label")
        self.label.setFont(font1)

        self.gridLayout_8.addWidget(self.label, 2, 4, 1, 1)

        self.linee_baseline = QLineEdit(self.groupBox_6)
        self.linee_baseline.setObjectName(u"linee_baseline")
        self.linee_baseline.setFont(font1)
        self.linee_baseline.setReadOnly(True)

        self.gridLayout_8.addWidget(self.linee_baseline, 2, 5, 1, 1)

        self.checkb_plot_diff = QCheckBox(self.groupBox_6)
        self.checkb_plot_diff.setObjectName(u"checkb_plot_diff")

        self.gridLayout_8.addWidget(self.checkb_plot_diff, 3, 4, 1, 1)

        self.btn_reset_baseline = QPushButton(self.groupBox_6)
        self.btn_reset_baseline.setObjectName(u"btn_reset_baseline")
        self.btn_reset_baseline.setFont(font2)

        self.gridLayout_8.addWidget(self.btn_reset_baseline, 3, 5, 1, 1)

        self.gridLayout_8.setColumnStretch(0, 2)
        self.gridLayout_8.setColumnStretch(1, 3)
        self.gridLayout_8.setColumnStretch(2, 2)
        self.gridLayout_8.setColumnStretch(3, 3)
        self.gridLayout_8.setColumnStretch(4, 2)
        self.gridLayout_8.setColumnStretch(5, 3)

        self.gridLayout_4.addWidget(self.groupBox_6, 2, 1, 1, 1)

        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setFont(font)
        self.gridLayout = QGridLayout(self.groupBox_5)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_21 = QLabel(self.groupBox_5)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font1)

        self.gridLayout.addWidget(self.label_21, 4, 2, 1, 1)

        self.label_23 = QLabel(self.groupBox_5)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font1)

        self.gridLayout.addWidget(self.label_23, 5, 0, 1, 1)

        self.label_24 = QLabel(self.groupBox_5)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font1)

        self.gridLayout.addWidget(self.label_24, 5, 2, 1, 1)

        self.checkb_enable_filter = QCheckBox(self.groupBox_5)
        self.checkb_enable_filter.setObjectName(u"checkb_enable_filter")
        self.checkb_enable_filter.setFont(font)

        self.gridLayout.addWidget(self.checkb_enable_filter, 4, 1, 1, 1)

        self.comb_debounce_cnt = QComboBox(self.groupBox_5)
        self.comb_debounce_cnt.setObjectName(u"comb_debounce_cnt")
        self.comb_debounce_cnt.setEnabled(False)
        self.comb_debounce_cnt.setFont(font1)

        self.gridLayout.addWidget(self.comb_debounce_cnt, 4, 5, 1, 1)

        self.comb_pad_conn = QComboBox(self.groupBox_5)
        self.comb_pad_conn.setObjectName(u"comb_pad_conn")
        self.comb_pad_conn.setFont(font1)

        self.gridLayout.addWidget(self.comb_pad_conn, 0, 5, 1, 1)

        self.label_13 = QLabel(self.groupBox_5)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font1)

        self.gridLayout.addWidget(self.label_13, 0, 4, 1, 1)

        self.label_16 = QLabel(self.groupBox_5)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font1)

        self.gridLayout.addWidget(self.label_16, 3, 4, 1, 1)

        self.comb_grade = QComboBox(self.groupBox_5)
        self.comb_grade.setObjectName(u"comb_grade")
        self.comb_grade.setEnabled(False)
        self.comb_grade.setFont(font1)

        self.gridLayout.addWidget(self.comb_grade, 3, 3, 1, 1)

        self.label_9 = QLabel(self.groupBox_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font1)

        self.gridLayout.addWidget(self.label_9, 0, 2, 1, 1)

        self.checkb_interrupt_mask_scandone = QCheckBox(self.groupBox_5)
        self.checkb_interrupt_mask_scandone.setObjectName(u"checkb_interrupt_mask_scandone")
        self.checkb_interrupt_mask_scandone.setEnabled(False)
        self.checkb_interrupt_mask_scandone.setFont(font1)

        self.gridLayout.addWidget(self.checkb_interrupt_mask_scandone, 6, 4, 1, 1)

        self.checkb_interrupt_mask_timeout = QCheckBox(self.groupBox_5)
        self.checkb_interrupt_mask_timeout.setObjectName(u"checkb_interrupt_mask_timeout")
        self.checkb_interrupt_mask_timeout.setEnabled(False)
        self.checkb_interrupt_mask_timeout.setFont(font1)

        self.gridLayout.addWidget(self.checkb_interrupt_mask_timeout, 6, 5, 1, 1)

        self.comb_refh = QComboBox(self.groupBox_5)
        self.comb_refh.setObjectName(u"comb_refh")
        self.comb_refh.setFont(font1)

        self.gridLayout.addWidget(self.comb_refh, 1, 1, 1, 1)

        self.comb_smh_lvl = QComboBox(self.groupBox_5)
        self.comb_smh_lvl.setObjectName(u"comb_smh_lvl")
        self.comb_smh_lvl.setEnabled(False)
        self.comb_smh_lvl.setFont(font1)

        self.gridLayout.addWidget(self.comb_smh_lvl, 5, 5, 1, 1)

        self.checkb_enable_denoise = QCheckBox(self.groupBox_5)
        self.checkb_enable_denoise.setObjectName(u"checkb_enable_denoise")
        self.checkb_enable_denoise.setFont(font)

        self.gridLayout.addWidget(self.checkb_enable_denoise, 3, 1, 1, 1)

        self.label_26 = QLabel(self.groupBox_5)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font1)

        self.gridLayout.addWidget(self.label_26, 6, 0, 1, 1)

        self.comb_fmode = QComboBox(self.groupBox_5)
        self.comb_fmode.setObjectName(u"comb_fmode")
        self.comb_fmode.setEnabled(False)
        self.comb_fmode.setFont(font1)

        self.gridLayout.addWidget(self.comb_fmode, 4, 3, 1, 1)

        self.label_11 = QLabel(self.groupBox_5)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)

        self.gridLayout.addWidget(self.label_11, 1, 2, 1, 1)

        self.label_25 = QLabel(self.groupBox_5)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font1)

        self.gridLayout.addWidget(self.label_25, 5, 4, 1, 1)

        self.spin_sleep_cycle = QSpinBox(self.groupBox_5)
        self.spin_sleep_cycle.setObjectName(u"spin_sleep_cycle")
        self.spin_sleep_cycle.setFont(font1)

        self.gridLayout.addWidget(self.spin_sleep_cycle, 0, 1, 1, 1)

        self.comb_atten = QComboBox(self.groupBox_5)
        self.comb_atten.setObjectName(u"comb_atten")
        self.comb_atten.setFont(font1)

        self.gridLayout.addWidget(self.comb_atten, 1, 5, 1, 1)

        self.comb_noise_thr = QComboBox(self.groupBox_5)
        self.comb_noise_thr.setObjectName(u"comb_noise_thr")
        self.comb_noise_thr.setEnabled(False)
        self.comb_noise_thr.setFont(font1)

        self.gridLayout.addWidget(self.comb_noise_thr, 5, 1, 1, 1)

        self.checkb_interrupt_mask_active = QCheckBox(self.groupBox_5)
        self.checkb_interrupt_mask_active.setObjectName(u"checkb_interrupt_mask_active")
        self.checkb_interrupt_mask_active.setEnabled(False)
        self.checkb_interrupt_mask_active.setFont(font1)

        self.gridLayout.addWidget(self.checkb_interrupt_mask_active, 6, 2, 1, 1)

        self.comb_cap_level = QComboBox(self.groupBox_5)
        self.comb_cap_level.setObjectName(u"comb_cap_level")
        self.comb_cap_level.setEnabled(False)
        self.comb_cap_level.setFont(font1)

        self.gridLayout.addWidget(self.comb_cap_level, 3, 5, 1, 1)

        self.label_12 = QLabel(self.groupBox_5)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font1)

        self.gridLayout.addWidget(self.label_12, 1, 4, 1, 1)

        self.label_14 = QLabel(self.groupBox_5)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font1)

        self.gridLayout.addWidget(self.label_14, 3, 0, 1, 1)

        self.checkb_enable_enable_interrupt = QCheckBox(self.groupBox_5)
        self.checkb_enable_enable_interrupt.setObjectName(u"checkb_enable_enable_interrupt")
        self.checkb_enable_enable_interrupt.setFont(font)

        self.gridLayout.addWidget(self.checkb_enable_enable_interrupt, 6, 1, 1, 1)

        self.label_22 = QLabel(self.groupBox_5)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font1)

        self.gridLayout.addWidget(self.label_22, 4, 4, 1, 1)

        self.spin_meas_times = QSpinBox(self.groupBox_5)
        self.spin_meas_times.setObjectName(u"spin_meas_times")
        self.spin_meas_times.setFont(font1)

        self.gridLayout.addWidget(self.spin_meas_times, 0, 3, 1, 1)

        self.checkb_interrupt_mask_inactive = QCheckBox(self.groupBox_5)
        self.checkb_interrupt_mask_inactive.setObjectName(u"checkb_interrupt_mask_inactive")
        self.checkb_interrupt_mask_inactive.setEnabled(False)
        self.checkb_interrupt_mask_inactive.setFont(font1)

        self.gridLayout.addWidget(self.checkb_interrupt_mask_inactive, 6, 3, 1, 1)

        self.comb_jitter_step = QComboBox(self.groupBox_5)
        self.comb_jitter_step.setObjectName(u"comb_jitter_step")
        self.comb_jitter_step.setEnabled(False)
        self.comb_jitter_step.setFont(font1)

        self.gridLayout.addWidget(self.comb_jitter_step, 5, 3, 1, 1)

        self.label_20 = QLabel(self.groupBox_5)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font1)

        self.gridLayout.addWidget(self.label_20, 4, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font1)

        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)

        self.label_8 = QLabel(self.groupBox_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)

        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)

        self.label_15 = QLabel(self.groupBox_5)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font1)

        self.gridLayout.addWidget(self.label_15, 3, 2, 1, 1)

        self.comb_refl = QComboBox(self.groupBox_5)
        self.comb_refl.setObjectName(u"comb_refl")
        self.comb_refl.setFont(font1)

        self.gridLayout.addWidget(self.comb_refl, 1, 3, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_5, 1, 1, 1, 1)

        self.gridLayout_4.setColumnStretch(0, 2)
        self.gridLayout_4.setColumnStretch(1, 3)
        self.gridLayout_4.setColumnStretch(2, 1)
        self.gridLayout_4.setColumnStretch(3, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tab_main.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ESP Touch Tool", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Plot", None))
        self.checkBox_12.setText(QCoreApplication.translate("MainWindow", u"CH12", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"CH4", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"CH5", None))
        self.checkBox_10.setText(QCoreApplication.translate("MainWindow", u"CH10", None))
        self.checkBox_13.setText(QCoreApplication.translate("MainWindow", u"CH13", None))
        self.checkBox_9.setText(QCoreApplication.translate("MainWindow", u"CH9", None))
        self.checkBox_14.setText(QCoreApplication.translate("MainWindow", u"CH14", None))
        self.checkBox_1.setText(QCoreApplication.translate("MainWindow", u"CH1", None))
        self.checkBox_6.setText(QCoreApplication.translate("MainWindow", u"CH6", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"CH3", None))
        self.checkBox_7.setText(QCoreApplication.translate("MainWindow", u"CH7", None))
        self.checkBox_8.setText(QCoreApplication.translate("MainWindow", u"CH8", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"CH2", None))
        self.checkBox_11.setText(QCoreApplication.translate("MainWindow", u"CH11", None))
        self.pushButton_plot_ctrl.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Trigger", None))
        self.checkBox_plot_trigger.setText(QCoreApplication.translate("MainWindow", u"Plot Trigger", None))
        self.tab_main.setTabText(self.tab_main.indexOf(self.tab_plot), QCoreApplication.translate("MainWindow", u"Plot", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Snd:", None))
        self.btn_clear_snd.setText(QCoreApplication.translate("MainWindow", u"Clear Snd", None))
        self.btn_log_sed.setText(QCoreApplication.translate("MainWindow", u"Send", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"Rcv:", None))
        self.label_snd_num.setText(QCoreApplication.translate("MainWindow", u"0000", None))
        self.btn_clear_rcv.setText(QCoreApplication.translate("MainWindow", u"Clear Rcv", None))
        self.label_rev_num.setText(QCoreApplication.translate("MainWindow", u"0000", None))
        self.tab_main.setTabText(self.tab_main.indexOf(self.tab_log), QCoreApplication.translate("MainWindow", u"Log", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Sleep Config", None))
        self.btn_reset_baseline_sleep.setText(QCoreApplication.translate("MainWindow", u"*Reset Baseline", None))
        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Value Diff", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Warkup value", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"*Measure Times", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"*Threshold Ratio", None))
        self.checkb_wakeup_keep_thres.setText(QCoreApplication.translate("MainWindow", u"Keep threshold", None))
        self.checkb_fix_threshold.setText(QCoreApplication.translate("MainWindow", u"Fixed threshold", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"*Sleep Cycle", None))
        self.btn_deepsleep.setText(QCoreApplication.translate("MainWindow", u"Deep sleep", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"*Warkup Chan", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Sleep baseline", None))
        self.btn_lightsleep.setText(QCoreApplication.translate("MainWindow", u"Light sleep", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"*Threshold value", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Sleep value", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Sampling freq", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.pushButton_pause.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.pushButton_choose_path.setText(QCoreApplication.translate("MainWindow", u"Choose", None))
        self.checkBox_file.setText(QCoreApplication.translate("MainWindow", u"Save in File", None))
        self.pushButton_chiprestart.setText(QCoreApplication.translate("MainWindow", u"Chip Restart", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Samples", None))
        self.pushButton_clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Channel Config", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Focus Chan", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Slope", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Initial Volt", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Thresh Ratio", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Diff Ratio", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Diff Max", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Raw", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Smooth", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"BaseLine", None))
        self.checkb_plot_diff.setText(QCoreApplication.translate("MainWindow", u"Plot Diff", None))
        self.btn_reset_baseline.setText(QCoreApplication.translate("MainWindow", u"Reset Baseline", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Global Config", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Noise Thrsh ", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Jitter Step", None))
        self.checkb_enable_filter.setText(QCoreApplication.translate("MainWindow", u"Enable", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Pad Conn", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Cap", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Measure Times", None))
        self.checkb_interrupt_mask_scandone.setText(QCoreApplication.translate("MainWindow", u"Scan done", None))
        self.checkb_interrupt_mask_timeout.setText(QCoreApplication.translate("MainWindow", u"Timeout", None))
        self.checkb_enable_denoise.setText(QCoreApplication.translate("MainWindow", u"Enable", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Hardware Events", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Low Volt", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Smooth Lv", None))
        self.checkb_interrupt_mask_active.setText(QCoreApplication.translate("MainWindow", u"Active", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Volt Atten", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Denoise", None))
        self.checkb_enable_enable_interrupt.setText(QCoreApplication.translate("MainWindow", u"Enable", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Debounce", None))
        self.checkb_interrupt_mask_inactive.setText(QCoreApplication.translate("MainWindow", u"Inactive", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"High Volt", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Sleep Cycle", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Grade", None))
    # retranslateUi

