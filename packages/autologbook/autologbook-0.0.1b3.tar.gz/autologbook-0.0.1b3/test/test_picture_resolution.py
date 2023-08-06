# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 21:02:36 2022

@author: Antonio
"""

import pytest

from autologbook.autoerror import WrongResolutionUnit
from autologbook.autotools import PictureResolution, ResolutionUnit


def test_creation():
    try:
        pr1 = PictureResolution(28.0, 28.0, ResolutionUnit.INCH)
    except (ValueError, WrongResolutionUnit):
        raise AssertionError

    with pytest.raises(ValueError):
        pr2 = PictureResolution(-1, 0, ResolutionUnit.INCH)

    with pytest.raises(WrongResolutionUnit):
        pr3 = PictureResolution(28.0, 28.0, 5)


def test_conversion():

    pr1 = PictureResolution(28., 28., ResolutionUnit.INCH)
    pr1.convert_to_unit(ResolutionUnit.CM)

    x, y, u = pr1.as_tuple()

    pr2 = PictureResolution(x, y, u)
    pr2.convert_to_unit(ResolutionUnit.INCH)

    assert pr1 == pr2
