# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 06:22:53 2022

@author: Antonio
"""

import random

import pytest
from PyQt5 import QtCore

from autologbook.autotools import UserRole


def test_userrole():

    # creation success
    for i in range(len(UserRole)):
        try:
            UserRole(QtCore.Qt.UserRole + 1 + i)
        except:
            # this should not happen!
            assert False

    # creation failures
    with pytest.raises(ValueError):
        UserRole(random.randint(0, QtCore.Qt.UserRole))

    # test minimum value
    for e in UserRole:
        assert e > QtCore.Qt.UserRole
