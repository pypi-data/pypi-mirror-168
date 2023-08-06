# !/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------
# ProjectName: Logcat Monitor
# Author: gentliu
# CreateTime: 30/7/2021 5:09 PM
# File Name: LogcatMonitor
# Description:
#   This is a tool class for use cases to find exception information in logcat in real time
# --------------------------------------------------------------
import json
import os
import subprocess
import time
from datetime import datetime

from logcat_monitor.statistics import Statistics
from logcat_monitor.threadpool import ThreadPool

# 缺省的异常捕捉关键字
KEYWORDS_DICT = {"ANR in ": "Anr",
                 "FATAL EXCEPTION:": "Fatal",
                 "signal 6": "Signal6",
                 "signal 7": "Signal7",
                 "signal 11": "Signal11",
                 "CRASH: ": "Crash",
                 "Force Closed": "ForceClose"}

# 捕捉到异常后截取的日志行数
INTERCEPTED_MAX_ROWS = 100

# 存放logcat日志文件的文件夹名
LOG_FOLDER_NAME = "logcats"

# 默认单个日志文件的大小
DEFAULT_LOGFILE_SIZE = 1024 * 1024 * 200


class LogcatMonitor:
    """
    Logcat 监控器
    """
    # 控制获取logcat停止的标志位
    _stop_logcat = True
    # 存储日志的缓冲区
    _logs = []
    _key_dict = KEYWORDS_DICT
    _pool = ThreadPool(1)
    _save_logcat = True
    _logfile_size = DEFAULT_LOGFILE_SIZE
    _log_file = None
    _write_log_file_size = 0

    def calculate_logfile_size(self, logfile_size: str):
        """
        根据字符串形式获得正式的文件大小数字
        :param logfile_size:
        :return:
        """
        self._logfile_size = DEFAULT_LOGFILE_SIZE
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        if logfile_size is None:
            length = 0
        else:
            length = len(logfile_size)
        if length > 0:
            unit = logfile_size[length - 1:]
            if unit.isdecimal():
                self._logfile_size = int(logfile_size)
            else:
                if length == 1:
                    value = 1
                else:
                    value = int("".join(list(filter(str.isdigit, logfile_size))))
                for i, s in enumerate(symbols):
                    if unit == s:
                        self._logfile_size = pow(1024, i + 1) * int(value)
                        break
                else:
                    print("Input log file size error, use default value")
        print("Logfile size: %s" % self._logfile_size)
        return self._logfile_size

    def __init__(self, serial_number=None, parent_folder=None, key_dict=None,
                 rows=INTERCEPTED_MAX_ROWS, logfile_size=None):
        self.calculate_logfile_size(logfile_size)
        if key_dict is not None:
            for key in key_dict:
                self._key_dict[key] = (key_dict[key])
        self._rows = rows
        # Create folder
        if parent_folder is None:
            self._self_folder = os.getcwd() + os.sep + LOG_FOLDER_NAME
        else:
            self._self_folder = parent_folder + os.sep + LOG_FOLDER_NAME
        if not os.path.isdir(self._self_folder):
            os.makedirs(self._self_folder)
        # Store serial number
        self._serial_number = serial_number
        # Statistics
        self._statistics = Statistics()

    def start_monitor(self, save_logcat=True):
        """
            Start logcat monitor
        :return:
        """
        self._stop_logcat = False
        self._save_logcat = save_logcat
        print("Start monitor _logcat")
        self._pool.add_task(self._filter_keyword)

    def stop_monitor(self):
        """
            Stop logcat monitor
        :return:
        """
        if self._stop_logcat:
            print("There are no tasks in progress")
        else:
            try:
                # Save statistics
                self._save_statistics()
                print("Stopping monitor\n")
                self._stop_logcat = True
                time.sleep(5)
                self._pool.destroy()
                time.sleep(3)
                print("Pool destroy")
            except Exception as ex:
                print(ex)

    def filter_file(self, file_name):
        """
        过滤文件
        :param file_name: 文件名称
        """
        intercept = False
        rows = 0
        keys = self._key_dict.keys()
        find_key = None
        line_count = 0
        with open(file_name, 'r', encoding='utf-8') as log_file:
            line = log_file.readline()
            while line:
                line_count += 1
                if not intercept:
                    # Read data normally
                    for key in keys:
                        if line.find(key) != -1:
                            message = "Detected：%s\n" % key
                            print(message)
                            self._logs.clear()
                            intercept = True
                            self._logs.append(line)
                            rows = 1
                            find_key = key
                else:
                    # An error has been detected.
                    # Read the subsequent qualified logs
                    if rows < self._rows:
                        # Add the current line to the logs
                        self._logs.append(line)
                        rows += 1
                    else:
                        # Finished reading the required logs
                        intercept = False
                        rows = 0
                        # Increase error counter
                        self._statistics.increase(self._key_dict, find_key)
                        # Save as a file
                        self._save_file(find_key, self._logs)
                line = log_file.readline()
        # Save statistics
        self._save_statistics()

    def create_new_logfile(self):
        """
        创建一个新的文件，用来保存日志
        """
        string_time = datetime.now().strftime("%Y%m%d%H%M%S")
        logcat_file_name = "%s%slogcat_%s.txt" % (self._self_folder, os.sep, string_time)
        self.close_logfile()
        self._log_file = open(logcat_file_name, 'w+', encoding='utf-8')
        self._write_log_file_size = 0

    def close_logfile(self):
        """
        关闭打开的日志文件
        """
        if self._log_file is not None and not self._log_file.closed:
            self._log_file.close()

    def _filter_keyword(self):
        """
            Keep reading logcat output, find error information.
            Count the number and write relevant information to the file
        :return:
        """
        print("Start monitor _logcat")
        # Initializing local variables
        self._logcat_clear()
        intercept = False
        rows = 0
        keys = self._key_dict.keys()
        find_key = None
        # File storage location(file full path)
        print("####### START LOGCAT WRITE #######")
        line_count = 0
        # Open logcat file
        if self._save_logcat:
            self.create_new_logfile()
        while not self._stop_logcat:
            print("Get logcat")
            # Keep reading data
            with self._logcat() as sub:
                for line in sub.stdout:
                    # Whether stop reading logcat
                    if self._stop_logcat:
                        # Normal termination
                        # Stop
                        print("####### STOP LOGCAT #######")
                        break
                    line_count += 1
                    try:
                        line_str = line.decode(encoding="utf-8", errors="ignore")
                    except Exception as ex:
                        print(ex)
                        line_str = str(ex)
                    # 检查文件是否超过限定的大小
                    if self._write_log_file_size > self._logfile_size:
                        self.create_new_logfile()

                    # Write logcat file
                    if self._log_file is not None and not self._log_file.closed:
                        self._log_file.write(line_str)
                        self._write_log_file_size += len(line_str)

                    if not intercept:
                        # Read data normally
                        for key in keys:
                            if line_str.find(key) != -1:
                                message = "Detected：%s\n" % key
                                print(message)
                                self._logs.clear()
                                intercept = True
                                self._logs.append(line_str)
                                rows = 1
                                find_key = key
                    else:
                        # An error has been detected.
                        # Read the subsequent qualified logs
                        if rows < self._rows:
                            # Add the current line to the logs
                            self._logs.append(line_str)
                            rows += 1
                        else:
                            # Finished reading the required logs
                            intercept = False
                            rows = 0
                            # Increase error counter
                            self._statistics.increase(self._key_dict, find_key)
                            # Save as a file
                            self._save_file(find_key, self._logs)

                print("End monitor _logcat")
                sub.kill()
                # Close logcat file
                self.close_logfile()
                if not self._stop_logcat:
                    # Abnormal termination
                    # wait...
                    time.sleep(2)

        print("####### END LOGCAT WRITE #######")

    def _logcat_clear(self):
        """
            Clear logcat
        :return:
        """
        if self._serial_number is not None and self._serial_number != "":
            cmd = "adb -s " + self._serial_number + " logcat -c"
        else:
            cmd = "adb logcat  -c"
        subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)

    def _logcat(self):
        """
            _logcat continuously outputs logs
        :return:
        """
        if self._serial_number is not None and self._serial_number != "":
            cmd = "adb -s " + self._serial_number + " logcat -v time"
        else:
            cmd = "adb logcat -v time"
        sub = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        return sub

    def _save_file(self, key, logs):
        """
            Save logs to file by key
        :param key:
        :param logs:
        :return:
        """
        if key is None:
            return
        # Key should in self._key_dict
        if key in self._key_dict:
            prefix = self._key_dict[key]
            # File storage location(file full path)
            file_name = "%s%s%s_%s.txt" % (self._self_folder, os.sep, prefix, datetime.now().strftime("%Y%m%d%H%M%S%f"))
            # Save to file
            # log is bytes, so mode set to wb
            with open(file_name, mode="w", encoding='utf-8') as f:
                for log in logs:
                    f.write(log)

    def _save_statistics(self):
        """
            Save the counted number of errors to the file statistics.txt
        :return:
        """
        print("Save Statistics")
        # File storage location(file full path)
        file_name = "%s%sstatistics.txt" % (self._self_folder, os.sep)
        # Convert self._statistics to json
        json_content = json.dumps(self._statistics.__dict__, ensure_ascii=False)
        # Save to file
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(json_content)
            print("Save Statistics Success")
