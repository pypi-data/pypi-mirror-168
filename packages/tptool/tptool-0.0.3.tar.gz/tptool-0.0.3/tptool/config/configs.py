from enum import Enum

class SysConfig:
    """
    Common constants for the application.
    """
    app_title = "TPtool"
    app_version = '0.0.1'
    app_export_path = "data"
    app_sources = ["Serial", "Simulator"]
    app_encoding = "utf-8"

    plot_update_ms = 10
    table_update_ms = 10
    param_update_ms = 100
    process_join_timeout_ms = 1000

    samples_buffer_size = 800
    serial_default_speed = 921600
    serial_timeout_s = 0.5
    parser_timeout_s = 0.005
    chip_boot_time_s = 1 #~1s
    simulator_default_speed = 0.002

    csv_filename = "%Y-%m-%d_%H-%M-%S"
    csv_delimiter = ","
    csv_extension = ".csv"

    log_filename = "{}.log".format(app_title)
    log_max_bytes = 51200
    log_level_debug = True
    log_default_to_console = True

    #touch communicate data format
    table_trigger_format = ["rb"]
    table_format = ["tb"]
    data_format = ["vl", "time", "channel", "raw", "smooth", "base"]
    trigger_format = ["tg", "time", "channel", "value", "active", "inactive", "done", "scan_done", "timeout"]
    config_format = ["cf", "time", "channel", "key", "type", "value"]
    config_channel_index = config_format.index("channel")
    config_key_index = config_format.index("key")
    config_type_index = config_format.index("type")
    config_value_index = config_format.index("value")
    data_time_index = data_format.index("time")
    data_channel_index = data_format.index("channel")
    data_data_index = data_format.index("raw")
    data_smooth_index = data_format.index("smooth")
    data_base_index = data_format.index("base")
    trigger_table_size = 10000
    trigger_time_index = trigger_format.index("time")
    trigger_channel_index = trigger_format.index("channel")
    trigger_value_index = trigger_format.index("value")
    trigger_active_index = trigger_format.index("active")
    trigger_inactive_index = trigger_format.index("inactive") 


    plot_xlabel_title = "Time"
    plot_xlabel_unit = "ms"
    plot_colors = ['#0c1ee8', '#76e80c', '#e8250c']
    plot_legends = ['raw value', 'smooth value', 'baseline value']
    plot_max_channels = 14
    diff_channel = 16
    #max lines: number of lines in each group
    plot_max_lines = len(plot_colors)

class TpCommand:
    #touch communicate command format
    #ch,slope,opt
    cmd_fmt_meas_channel = "tpcfg -e {} -e {} -e {}"
    #sleep_cycle,meas_times,refh,refl,atten,pad_conn,enable_denoise,grade,cap_level
    cmd_fmt_meas_global = "tpcfg -m {} -m {} -m {} -m {} -m {} -m {} -m {} -m {} -m {}"
    #ch, enable, int(ratio*1000)
    cmd_fmt_judge_channel = "tpcfg -t {} -t {} -t {}"
    #enable_filter,fmode,debounce_cnt,noise_thr,jitter_step,smh_lvl,enable_interrupt,interrupt_mask
    cmd_fmt_judge_global = "tpcfg -j {} -j {} -j {} -j {} -j {} -j {} -j {} -j {}"
    cmd_fmt_reset_baseline = "tpctrl -r 1 -c {}" #channel_mask
    #channel_mask, sleep_cycle_sleep, meas_times_sleep, threshold_ratio_sleep, fix_threshold
    cmd_fmt_enter_deep_sleep = "tpctrl -c {} -l 2 -l {} -l {} -l {} -l {}"
    cmd_fmt_enter_light_sleep = "tpctrl -l 1 -c {}" #channel_mask
    cmd_fmt_chip_restart = "restart"
    #speed_ms, channel_mask
    cmd_fmt_output_enable = "tpctrl -o {} -c {}"
    @classmethod
    def cmd_meas_channel(cls,ch=-1,slope=-1,opt=-1):
        return cls.cmd_fmt_meas_channel.format(ch,slope,opt)
    @classmethod    
    def cmd_meas_global(cls,sleep_cycle=-1,meas_times=-1,refh=-1,refl=-1,atten=-1,pad_conn=-1,enable_denoise=0,grade=-1,cap_level=-1):
        return cls.cmd_fmt_meas_global.format(sleep_cycle,meas_times,refh,refl,atten,pad_conn,enable_denoise,grade,cap_level)
    @classmethod
    def cmd_judge_channel(cls, ch=-1, enable=1, threshold_ratio=0.0):
        return cls.cmd_fmt_judge_channel.format(ch, enable, int(threshold_ratio*1000))
    @classmethod
    def cmd_judge_global(cls, enable_filter=0,fmode=-1,debounce_cnt=-1,noise_thr=-1,jitter_step=-1,smh_lvl=-1,enable_interrupt=0,interrupt_mask=0):
        return cls.cmd_fmt_judge_global.format(enable_filter,fmode,debounce_cnt,noise_thr,jitter_step,smh_lvl,enable_interrupt,interrupt_mask)
    @classmethod
    def cmd_reset_baseline(cls, channel_mask=0):
        return cls.cmd_fmt_reset_baseline.format(channel_mask)
    @classmethod
    def cmd_enter_deep_sleep(cls, channel_mask=0, sleep_cycle_sleep=0, meas_times_sleep=0, threshold_ratio_sleep=0.0, fix_threshold=0):
        return cls.cmd_fmt_enter_deep_sleep.format(channel_mask, sleep_cycle_sleep, meas_times_sleep, int(threshold_ratio_sleep*1000), fix_threshold)
    @classmethod
    def cmd_enter_light_sleep(cls, channel_mask=0):
        return cls.cmd_fmt_enter_light_sleep.format(channel_mask)
    @classmethod
    def cmd_chip_restart(cls):
        return cls.cmd_fmt_chip_restart
    @classmethod
    def cmd_output_enable(cls, speed_ms=-1, channel_mask=0):
        return cls.cmd_fmt_output_enable.format(speed_ms, channel_mask)

class TpConfig:
    class Touch:
        channels = {"min":1, "max":14, "dflt":1, 0:"None", 1:"CH1", 2:"CH2", 3:"CH3", 4:"CH4", 5:"CH5", 6:"CH6", 7:"CH7", 8:"CH8", 9:"CH9", 10:"CH10", 11:"CH11", 12:"CH12", 13:"CH13", 14:"CH14"}
        sample_freq = {"min":1, "max":50, "dflt":50} #output freq
        sleep_mode = {"light":1, "deep":2}
    class SleepParam:
        sleep_cycle = {"min":0, "max":0xffff, "dflt":100} # 100 ~= 1ms
        meas_times = {"min":0, "max":5000, "dflt":500} # 100 ~= 2ms
        enable_fixed_threshold = {"min":0, "max":1, "dflt":0, 0:"disable", 1:"enable"}
        threshold_value = {"min":0.001, "max":10000, "dflt":150}
        threshold_ratio = {"min":0.001, "max":1.000, "dflt":0.020}
    class MeasGlobal:
        sleep_cycle = {"min":0, "max":0xff, "dflt":0xf}
        meas_times = {"min":0, "max":5000, "dflt":500}
        refh = {"min":0, "max":3, "dflt":3, 0:"2.4v", 1:"2.5v", 2:"2.6v", 3:"2.7v"}
        refl = {"min":0, "max":3, "dflt":0, 0:"0.5v", 1:"0.6v", 2:"0.7v", 3:"0.8v"}
        atten = {"min":0, "max":3, "dflt":2, 0:"1.5v", 1:"1.0v", 2:"0.5v", 3:"0v"}
        pad_conn = {"min":0, "max":1, "dflt":1, 0:"highz", 1:"gnd"}
        enable_denoise = {"min":0, "max":1, "dflt":0, 0:"disable", 1:"enable"}
        grade = {"min":0, "max":3, "dflt":3, 0:"bit12", 1:"bit10", 2:"bit8", 3:"bit4"}
        cap_level = {"min":0, "max":7, "dflt":4, 0:"L0 5pf", 1:"L1 6.4pf", 2:"L2 7.8pf", 3:"L3 9.2pf", 4:"L4 10.6pf", 5:"L5 12.0pf", 6:"L6 13.4pf", 7:"L7 14.8pf"}
    class MeasChannel:
        #BUG: if chose 0, slope will always 0 until hardware reset
        slope = {"min":1, "max":7, "dflt":7, 0:"None", 1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7"}
        opt = {"min":0, "max":1, "dflt":0, 0:"low", 1:"high"}
    class JudgeGlobal:
        enable_filter = {"min":0, "max":1, "dflt":0, 0:"disable", 1:"enable"}
        mode = {"min":0, "max":6, "dflt":2, 0:"IIR_4", 1:"IIR_8", 2:"IIR_16", 3:"IIR_32", 4:"IIR_64", 5:"IIR_128", 6:"IIR_256", 7:"Jitter"}
        debounce_cnt = {"min":0, "max":7, "dflt":1, 0:"1", 1:"2", 2:"3", 3:"4", 4:"5", 5:"6", 6:"7", 7:"8"} #n+1
        noise_thr = {"min":0, "max":3, "dflt":0, 0:"4/8", 1:"3/8", 2:"2/8", 3:"1"}
        jitter_step = {"min":0, "max":15, "dflt":4, 0:"0", 1:"1", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 10:"10", 11:"11", 12:"12", 13:"13", 14:"14", 15:"15"}
        smh_lvl = {"min":0, "max":3, "dflt":1, 0:"off", 1:"IIR_2", 2:"IIR_4", 3:"IIR_8"}
        enable_interrupt = {"min":0, "max":1, "dflt":0, 0:"disable", 1:"enable"}
        interrupt_mask = {"min":0, "max":0b11110, "dflt":0b00110}
    class JudgeChannel:
        enable_handler = {"min":0, "max":1, "dflt":1, 0:"disable", 1:"enable"}
        threshold_ratio = {"min":0.001, "max":1.000, "dflt":0.020}
    class Current:
        param = {"sample_freq":-1,"touch_init":-1, "enable_mask":-1, "sleep_cycle":-1, "meas_times":-1,\
            "refh":-1, "refl":-1, "atten":-1, "pad_conn":-1, "enable_denoise":-1, "grade":-1, "cap_level":-1,\
            "benchmark_reset":[-1 for _ in range(SysConfig.plot_max_channels+1)],\
            "pad_enable":[-1 for _ in range(SysConfig.plot_max_channels+1)],\
            "slope":[-1 for _ in range(SysConfig.plot_max_channels+1)],\
            "opt":[-1 for _ in range(SysConfig.plot_max_channels+1)],\
            "threshold_ratio":[-1 for _ in range(SysConfig.plot_max_channels+1)],\
            "threshold_value":[-1 for _ in range(SysConfig.plot_max_channels+1)],\
            "timeout_meas":-1, "enable_filter":-1, "mode":-1,\
            "debounce_cnt":-1, "noise_thr":-1, "jitter_step":-1, "smh_lvl":-1,\
            "enable_interrupt":-1, "interrupt_mask":-1,\
            "pad_fsm_start":-1, "output_meas":0,\
            "enable_nvs":-1, "write_nvs":-1, "read_nvs":-1, "nvs_magic_number":-1,\
            "enable_console":-1, "enable_esp_now":-1, "enable_buzzer":-1, "buzzer_io":-1,\
            "buzzer_enable_io":-1,\
            "in_deepsleep": [-1 for _ in range(SysConfig.plot_max_channels+1)],\
            "threshold_deepsleep": [-1 for _ in range(SysConfig.plot_max_channels+1)],\
            "threshold_ratio_deepsleep":[-1 for _ in range(SysConfig.plot_max_channels+1)],\
            "smooth_deepsleep":[-1 for _ in range(SysConfig.plot_max_channels+1)],\
            "baseline_deepsleep":[-1 for _ in range(SysConfig.plot_max_channels+1)],\
            "smooth_deepsleep_out":[-1 for _ in range(SysConfig.plot_max_channels+1)],\
            "baseline_deepsleep_out":[-1 for _ in range(SysConfig.plot_max_channels+1)],
            "diff_deepsleep_out":[-1 for _ in range(SysConfig.plot_max_channels+1)]}


class SourceType(Enum):
    """
    Enum for the types of sources. Indices MUST match app_sources constant.
    """
    simulator = 1
    serial = 0


class MinimalPython:
    """
    Specifies the minimal Python version required.
    """
    major = 3
    minor = 6
    release = 0
