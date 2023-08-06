#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/9/14 11:24
# @Author  : zhangbc0315@outlook.com
# @File    : fast_log.py
# @Software: PyCharm

import logging
import datetime
import sys


class FastLog:

    def __init__(self, log_fp: str, log_level: str):
        """
        :param log_fp: file path to save log
        :param log_level: 'CRITICAL','FATAL','ERROR','WARN','WARNING','INFO','DEBUG','NOTSET'
        """
        if log_level not in ['CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']:
            raise ValueError(f"Only these values can be selected for log_level: "
                             f"\n'CRITICAL','FATAL','ERROR','WARN','WARNING','INFO','DEBUG','NOTSET'."
                             f"\nBut get {log_level}")
        self._logger = logging.getLogger('FastLogger')
        self._logger.setLevel(log_level)

        s_handler = logging.StreamHandler(sys.stderr)
        s_handler.setLevel(log_level)
        s_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(message)s"))

        f_handler = logging.FileHandler(log_fp)
        f_handler.setLevel(log_level)
        f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

        self._logger.addHandler(s_handler)
        self._logger.addHandler(f_handler)

    @property
    def logger(self) -> logging.Logger:
        return self._logger


if __name__ == "__main__":
    pass
