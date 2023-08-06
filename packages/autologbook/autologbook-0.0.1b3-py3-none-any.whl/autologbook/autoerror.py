# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 08:13:29 2022

@author: elog-admin
"""


class AutologError(Exception):
    """Base class for autologbook exception."""

    pass


class SampleError(AutologError):
    """Base Sample Error."""


class NotAValidConfigurationFile(AutologError):
    """Invalid configuration file."""


class ParentSampleError(SampleError):
    """
    Error with the sample parent.

    Raised when an error with the parent genealogy occurs.
    """

    pass


class SampleNameAlreadyExisting(SampleError):
    """
    Error with the Sample name.

    A top level sample must have an unique name.

    Raised when a sample with the same name of another sample is added.
    """

    pass


class ProtocolError(AutologError):
    """Base Protocol Error."""

    pass


class MissingProtocolInformation(ProtocolError):
    """
    Missing protocol information.

    Raised when attempting to build a protocol without providing all
    needed information.
    """

    pass


class ElogError(AutologError):
    """Base ELOG Error."""

    pass


class ReadOnlyEntry(ElogError):
    """
    Read only entry.

    Raised when an attempt is made to write or delete a read-only elog
    entry.
    """

    pass


class MissingWorkerParameter(AutologError):
    """
    Missing worker parameter.

    Raised when attempting to update a worker parameters without providing
    a needed parameter.
    """

    pass


class MicroscopePictureError(AutologError):
    """Generic error associated with a Microscope picture."""

    pass


class WrongResolutionUnit(MicroscopePictureError):
    """
    Wrong resolution unit.

    Raised when an attempt to use an invalide unit of measurements for the
    picture resolution is made.
    """

    pass


class ImpossibleToConvert(MicroscopePictureError):
    """Impossible to convert image resolution w/o unit of measurements."""

    pass


class NotFEIMicroscopePicture(MicroscopePictureError):
    """
    Not a FEI microscope picture.

    Raised when an attempt is made to constructur a FEIPicture with a TIFF
    picture not generated from a FEI microscope
    """

    pass
