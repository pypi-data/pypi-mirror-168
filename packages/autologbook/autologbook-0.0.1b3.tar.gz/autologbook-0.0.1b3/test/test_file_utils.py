# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 15:40:04 2022

@author: elog-admin
"""

from pathlib import Path

from autologbook.autotools import DateType, get_date_from_file, pretty_filesize


def test_filesize():
    file = Path(__file__)
    size = file.stat().st_size
    print(f'This file size is {pretty_filesize(size)}')


def test_date_from_file():
    file = Path(__file__)
    get_date_from_file(file.stat(), DateType.ATIME)
    get_date_from_file(file.stat(), DateType.CTIME)
    get_date_from_file(file.stat(), DateType.MTIME)

    # print(f'{atime:%Y-%m-%d %H:%M:%S}')
    # print(f'{ctime:%Y-%m-%d %H:%M:%S}')
    # print(f'{mtime:%Y-%m-%d %H:%M:%S}')
