# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 14:22:06 2022

@author: elog-admin
"""

import logging
from pathlib import Path

#
# LOGGING PARAMETERS
#
LEVELS = {'debug': logging.DEBUG,
          'vipdebug': logging.INFO - 5,
          'info': logging.INFO,
          'warn': logging.WARNING,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

#
# GENERAL
#
CUSTOMID_START = 1000
CUSTOMID_TIFFCODE = 37510
VERSION = '0.0.1.b.3'
#
# ELOG PARAMETERS
#
ELOG_USER = 'log-robot'
ELOG_PASSWORD = 'mTZtK2iFHhwqixkhJV0JkplSqMMu9ykWOhcNY/1WyL7'
ELOG_HOSTNAME = 'https://10.166.16.24'
ELOG_PORT = 8080
MAX_AUTH_ERROR = 5
USE_SSL = True
#
# EXTERNAL TOOLS
#
NOTEPAD_BEST = Path("C:\\Program Files\\Notepad++\\notepad++.exe")
ROBOCOPY_EXE = Path("C:\\Windows\\System32\\Robocopy.exe")
#
# WATCHDOGS
#
AUTOLOGBOOK_WATCHDOG_MAX_ATTEMPTS = 5
AUTOLOGBOOK_WATCHDOG_WAIT_MIN = 1
AUTOLOGBOOK_WATCHDOG_WAIT_MAX = 5
AUTOLOGBOOK_WATCHDOG_WAIT_INCREMENT = 1
AUTOLOGBOOK_WATCHDOG_MIN_DELAY = 45
AUTOLOGBOOK_WATCHDOG_TIMEOUT = 0.5
IMAGEFILE_MATCHING_PATTERNS = [r'^.*\.[Tt][Ii][Ff]{1,2}?$']
IMAGEFILE_EXCLUDE_PATTERNS = [
    r'^.*[Cc][Rr][Oo][Pp]{1,2}[Ee]?[Dd}?[\s\S]*[-_][Cc][Rr][Oo][Pp]{1,2}[Ee]?[Dd]?\.[Tt][Ii][Ff]{1,2}$']
ATTACHMENT_MATCHING_PATTERNS = [r'^.*\.[Pp][Dd][Ff]$',
                                r'^.*\.[Dd][Oo][Cc][Xx]?$',
                                r'^.*\.[Xx][Ll][Ss][XxMm]?$']
ATTACHMENT_EXCLUDE_PATTERNS = None
YAMLFILE_MATCHING_PATTERNS = [r'^.*\.[Yy][Aa]?[Mm][Ll]']
YAMLFILE_EXCLUDE_PATTERNS = None
NAVIGATION_MATCHING_PATTERNS = [
    r'^.*[Nn][Aa][Vv][Ii]?[Gg]?[Aa]?[Tt]?[Ii]?[Oo]?[Nn]?[-_\s]?[Cc][Aa][Mm][Ee]?[Rr]?[Aa]?']
NAVIGATION_EXCLUDE_PATTERNS = None

#
# MIRRORING WATCHDOG
#
AUTOLOGBOOK_MIRRORING_MAX_ATTEMPTS = 2
AUTOLOGBOOK_MIRRORING_WAIT = 0.5
AUTOLOGBOOK_MIRRORING_TIMEOUT = 0.2
#
# IMAGESERVER
#
IMAGE_SERVER_BASE_PATH = Path('R:\\A226\\Results')
IMAGE_SERVER_ROOT_URL = 'https://10.166.16.24/micro'
IMAGE_SAMPLE_THUMB_MAX_WIDTH = 400
#
# FEI
#
FEI_AUTO_CALIBRATION = True
FEI_DATABAR_REMOVAL = False
#
# QUATTRO
#
IMAGE_NAVIGATION_MAX_WIDTH = 500
QUATTRO_LOGBOOK = 'Quattro-Analysis'
#
# VERSA
#
VERSA_LOGBOOK = 'Versa-Analysis'


def __getattr__(name):
    return globals()[name]
