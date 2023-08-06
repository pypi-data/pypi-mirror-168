# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 11:06:58 2022

@author: elog-admin
"""

import configparser
import glob
import logging
import math
import os
import re
import shutil
from datetime import datetime, timezone
from enum import Enum, IntEnum, auto
from pathlib import Path
from typing import Any

import PIL.TiffImagePlugin
import elog
import yaml
from dateutil import tz
from PIL.TiffImagePlugin import ImageFileDirectory_v2
from PyQt5 import QtCore

from autologbook import autoconfig, autoerror

log = logging.getLogger('__main__')


def init(config):
    """
    Initialize module wide global variables.

    Parameters
    ----------
    config : configparser object or string corresponding to a configuration file
        The configuration object

    Returns
    -------
    None.

    """
    _config = configparser.ConfigParser()
    if isinstance(config, configparser.ConfigParser):
        _config = config
    elif isinstance(config, str):
        if Path(config).exists() and Path(config).is_file():
            _config.read(config)
        else:
            raise ValueError('Unable to initialize the autowatch-gui module because '
                             + 'the provided configuration file (%s) doesn\'t exist' %
                             config)
    elif isinstance(config, Path):
        if config.exists() and config.is_file():
            _config.read(str(config))
        else:
            raise ValueError(
                'Unable to initialize the autowatch-gui module because the provided '
                + 'configuration file (%s) doesn\'t exist' % config)
    else:
        raise TypeError(
            'Unable to initialize the autowatch-gui module because of wrong config file')

    # ELOG section
    autoconfig.ELOG_USER = _config.get(
        'elog', 'elog_user', fallback=autoconfig.ELOG_USER)
    autoconfig.ELOG_PASSWORD = _config.get(
        'elog', 'elog_password', fallback=autoconfig.ELOG_PASSWORD)
    autoconfig.ELOG_HOSTNAME = _config.get(
        'elog', 'elog_hostname', fallback=autoconfig.ELOG_HOSTNAME)
    autoconfig.ELOG_PORT = _config.getint(
        'elog', 'elog_port', fallback=autoconfig.ELOG_PORT)
    autoconfig.USE_SSL = _config.getboolean(
        'elog', 'use_ssl', fallback=autoconfig.USE_SSL)
    autoconfig.MAX_AUTH_ERROR = _config.getint(
        'elog', 'max_auth_error', fallback=autoconfig.MAX_AUTH_ERROR)

    # EXTERNAL TOOLS section
    autoconfig.NOTEPAD_BEST = Path(_config.get(
        'external tools', 'favourite text editor', fallback=autoconfig.NOTEPAD_BEST))
    autoconfig.ROBOCOPY_EXE = Path(_config.get(
        'external tools', 'robocopy', fallback=autoconfig.ROBOCOPY_EXE))

    # AUTOLOGBOOK WATCHDOG
    autoconfig.AUTOLOGBOOK_WATCHDOG_MAX_ATTEMPTS = _config.getint('Autologbook watchdog', 'max_attempts',
                                                                  fallback=autoconfig.AUTOLOGBOOK_WATCHDOG_MAX_ATTEMPTS)
    autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MIN = _config.getfloat('Autologbook watchdog', 'wait_min',
                                                                fallback=autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MIN)
    autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MAX = _config.getfloat('Autologbook watchdog', 'wait_max',
                                                                fallback=autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MAX)
    autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_INCREMENT = \
        _config.getfloat('Autologbook watchdog', 'wait_increment',
                         fallback=autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_INCREMENT)
    autoconfig.AUTOLOGBOOK_WATCHDOG_MIN_DELAY = \
        _config.getfloat('Autologbook watchdog', 'minimum delay between ELOG post',
                         fallback=autoconfig.AUTOLOGBOOK_WATCHDOG_MIN_DELAY)
    autoconfig.AUTOLOGBOOK_WATCHDOG_TIMEOUT = _config.getfloat('Autologbook watchdog', 'observer_timeout',
                                                               fallback=autoconfig.AUTOLOGBOOK_WATCHDOG_TIMEOUT)

    # MIRRORING WATCHDOG
    autoconfig.AUTOLOGBOOK_MIRRORING_MAX_ATTEMPTS = \
        _config.getint('Mirroring watchdog', 'max_attempts', fallback=autoconfig.AUTOLOGBOOK_MIRRORING_MAX_ATTEMPTS)
    autoconfig.AUTOLOGBOOK_MIRRORING_WAIT = _config.getfloat(
        'Mirroring watchdog', 'wait', fallback=autoconfig.AUTOLOGBOOK_MIRRORING_WAIT)
    autoconfig.AUTOLOGBOOK_MIRRORING_TIMEOUT = _config.getfloat('Mirroring watchdog', 'observer_timeout',
                                                                fallback=autoconfig.AUTOLOGBOOK_MIRRORING_TIMEOUT)

    # IMAGE SERVER
    autoconfig.IMAGE_SERVER_BASE_PATH = _config.get(
        'Image_server', 'base_path', fallback=autoconfig.IMAGE_SERVER_BASE_PATH)
    autoconfig.IMAGE_SERVER_ROOT_URL = _config.get(
        'Image_server', 'server_root', fallback=autoconfig.IMAGE_SERVER_ROOT_URL)
    autoconfig.IMAGE_SAMPLE_THUMB_MAX_WIDTH = _config.getint(
        'Image_server', 'image_thumb_width', fallback=autoconfig.IMAGE_SAMPLE_THUMB_MAX_WIDTH)
    autoconfig.CUSTOMID_START = _config.getint(
        'Image_server', 'custom_id_start', fallback=autoconfig.CUSTOMID_START)
    autoconfig.CUSTOMID_TIFFCODE = _config.getint(
        'Image_server', 'tiff_tag_code', fallback=autoconfig.CUSTOMID_TIFFCODE)

    # FEI
    autoconfig.FEI_AUTO_CALIBRATION = _config.getboolean(
        'FEI', 'auto_calibration', fallback=autoconfig.FEI_AUTO_CALIBRATION)
    autoconfig.FEI_DATABAR_REMOVAL = _config.getboolean(
        'FEI', 'databar_removal', fallback=autoconfig.FEI_DATABAR_REMOVAL)

    # Quattro Specific
    autoconfig.IMAGE_NAVIGATION_MAX_WIDTH = _config.getint(
        'Quattro', 'image_navcam_width', fallback=autoconfig.IMAGE_NAVIGATION_MAX_WIDTH)
    autoconfig.QUATTRO_LOGBOOK = _config.get(
        'Quattro', 'logbook', fallback=autoconfig.QUATTRO_LOGBOOK)

    # Versa Specific
    autoconfig.VERSA_LOGBOOK = _config.get(
        'Versa', 'logbook', fallback=autoconfig.VERSA_LOGBOOK)


def generate_default_conf():
    """
    Generate a default configuration object.

    Returns
    -------
    None.

    """
    config = configparser.ConfigParser(allow_no_value=True)
    config.add_section('elog')
    config['elog'] = {
        'elog_user': 'log-robot',
        'elog_password': encrypt_pass('IchBinRoboter'),
        'elog_hostname': 'https://10.166.16.24',
        'elog_port': '8080',
        'use_ssl': True,
        'use_encrypt_pwd': True,
        'max_auth_error': 5
    }
    config['external tools'] = {
        'favourite text editor': 'C:\\Program Files\\Notepad++\\notepad++.exe',
        'robocopy': shutil.which('robocopy.exe')
    }
    config['Quattro'] = {
        'logbook': 'Quattro-Analysis',
        'image_navcam_width': '500'
    }
    config['Versa'] = {
        'logbook': 'Versa-Analysis'
    }
    config['Mirroring engine'] = {
        'engine': 'watchdog'
    }
    config['Autologbook watchdog'] = {
        'max_attempts': '5',
        'wait_min': '1',
        'wait_max': '5',
        'wait_increment': '1',
        'minimum delay between ELOG post': '45',
        'observer_timeout': 0.5
    }
    config['Mirroring watchdog'] = {
        'max_attempts': '2',
        'wait': '0.5',
        'observer_timeout': 0.2
    }
    config['Image_server'] = {
        'base_path': 'R:\\A226\\Results',
        'server_root': 'https://10.166.16.24/micro',
        'image_thumb_width': 400,
        'custom_id_start': 1000,
        'tiff_tag_code': 37510
    }
    config['FEI'] = {
        'auto_calibration': True,
        'databar_removal': False
    }
    return config


def safe_configread(conffile):
    """
    Read the configuration file in a safe manner.

    This function is very useful to read in configuration file checking that
    all the relevant sections and options are there.

    The configuration file is read with the standard configparser.read method
    and a configuration object with all default sections and options is
    generated.

    The two configuration objects are compared and if a section in the read
    file is missing, then it is taken from the default.

    If any addition (section or option) was requested than the integrated
    configuration file is saved to the input file so that the same issue should
    not happen anymore.

    Parameters
    ----------
    conffile : path-like or string
        The filename of the configuration file to be read.

    Returns
    -------
    config : configparser.ConfigParser
        A ConfigParser object containing all sections and options required.

    """
    config = configparser.ConfigParser()
    config.read(conffile)

    conffile_needs_updates = False

    if not config.has_section('elog'):
        # very likely this is not an auto configuration file
        raise autoerror.NotAValidConfigurationFile(
            f'File {conffile} is not a valid configuration file.')

    # check if it is an old configuration file with plain text password
    if not config.has_option('elog', 'use_encrypt_pwd'):
        if not config.has_option('elog', 'elog_password'):
            config.set('elog', 'elog_password', encrypt_pass(
                config.get('elog', 'elog_password', fallback=' ')))
        conffile_needs_updates = True

    # now we must check that we have everything
    default_config = generate_default_conf()
    for section in default_config.sections():
        if not config.has_section(section):
            config.add_section(section)
            conffile_needs_updates = True
            log.info('Section %s is missing from configuration file %s.'
                     ' The default values will be used and the file updated' %
                     (section, conffile))
        for option in default_config.options(section):
            if not config.has_option(section, option):
                config.set(section, option, default_config[section][option])
                conffile_needs_updates = True
                log.info('Option %s from section %s is missing. The default value will be used and the file update' %
                         (option, section))

    if not config.getboolean('elog', 'use_encrypt_pwd'):
        # it looks like the user changed manually the configuration file introducing a
        # plain text password.
        # we need to hash the password and update the configuration file
        config['elog']['use_encrypt_pwd'] = "True"
        config['elog']['elog_password'] = encrypt_pass(
            config['elog']['elog_password'])
        conffile_needs_updates = True

    if conffile_needs_updates:
        write_conffile(config, conffile)

    return config


def write_default_conffile(filename='autolog-conf.ini'):
    """
    Write the default configuration object to a file.

    Parameters
    ----------
    filename : path-like object, optional
        The filename for the configuration file.
        The default is 'autolog-conf.ini'.

    Returns
    -------
    None.

    """
    write_conffile(generate_default_conf(), filename)


def write_conffile(config_object, filename):
    """
    Write a configuration object to a file.

    Parameters
    ----------
    config_object : ConfigParser
        The configuration dictionary to be dumped into a file.
    filename : str or path-like
        The output file name

    Returns
    -------
    None.

    """
    if not isinstance(config_object, configparser.ConfigParser):
        raise TypeError('Invalid configuration object')

    message = ('###  AUTOLOGBOOK CONFIGURATION FILE.\n'
               f'# Generated on {datetime.now():%Y-%m-%d %H:%M:%S}\n'
               f'# Autologbook version v{autoconfig.VERSION}\n'
               '# \n'
               '## IMPORTANT NOTE ABOUT PASSWORDS:\n'
               '# \n'
               '# If you need to change the password in this configuration file, just\n'
               '# enter the plain text password in the password field and set use_encrypt_pwd to False.\n'
               '# The next time that autologook is executed the plain text password will be hashed \n'
               '# and this configuration file will be updated with the hashed value for your security.\n'
               '# \n\n')

    with open(filename, 'w') as configfile:
        configfile.write(message)
        config_object.write(configfile)


def parents_list(actual_path, base_path):
    """
    Generate the parents list of a given image.

    This tool is used to generate of a list of parents pairs.
    Let's assume you are adding a new image with the following path:
        actual_path = R:/A226/Results/2022/123 - proj - resp/SampleA/SubSampleB/SubSampleC/image.tiff
    and that the protocol folder is located at:
        base_path = R:/A226/Results/2022/123 - proj - resp/

    This function is returning the following list:
        ['SampleA', 'SampleA/SubSampleB', 'SampleA/SubSampleB/SubSampleC']

    It is to say a list of all parents.

    Parameters
    ----------
    actual_path : string or Path
        The full path (including the filename) of the pictures being considered.
    base_path : string or Path
        The path of the protocol.

    Returns
    -------
    p_list : list
        A list of parent. See the function description for more details.

    """
    if not isinstance(actual_path, Path):
        actual_path = Path(actual_path)

    if not isinstance(base_path, Path):
        base_path = Path(base_path)

    full_name = str(actual_path.relative_to(
        base_path).parent).replace('\\', '/')

    p_list = []
    for i in range(len(full_name.split('/'))):
        element = "/".join(full_name.split("/")[0:i])
        if element != '':
            p_list.append(element)

    p_list.append(full_name)

    return p_list


def decode_command_output(text):
    """
    Decode the output of a command started with Popen.

    Parameters
    ----------
    text : STRING
        The text produced by Popen and to be decoded.

    Returns
    -------
    STRING
        The decoded text.

    """
    return '\n'.join(text.decode('utf-8').splitlines())


def ctname():
    """
    Return the current QThread name.

    Returns
    -------
    STRING
        The name of the current QThread.

    """
    return QtCore.QThread.currentThread().objectName()


# noinspection PyPep8Naming
class literal_str(str):
    """Type definition for the YAML representer."""

    pass


def change_style(style, representer):
    """
    Change the YAML dumper style.

    Parameters
    ----------
    style : String
        A string to define new style.
    representer : SafeRepresenter
        The yaml representer of which the style should be changed

    Returns
    -------
    Callable
        The new representer with the changed style.

    """

    def new_representer(dumper, data):
        """
        Return the new representer.

        Parameters
        ----------
        dumper : TYPE
            DESCRIPTION.
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        scalar : TYPE
            DESCRIPTION.

        """
        scalar = representer(dumper, data)
        scalar.style = style
        return scalar

    return new_representer


def my_excepthook(exc_type, exc_value, traceback, logger=log):
    """Define a customized exception hook.

    Instead of printing the output of an uncaught exception to the stderr,
    it is redirected to the logger. It is very practical because it will
    appear on the GUI

    Parameters
    ----------
    exc_type : TYPE
        The exception type.
    exc_value : TYPE
        The exception value.
    traceback : TYPE
        The whole traceback.
    logger : TYPE, optional
        The logger instance where the exception should be sent.
        The default is log.

    Returns
    -------
    None.

    """
    logger.error("Logging an uncaught exception",
                 exc_info=(exc_type, exc_value, traceback))


def encrypt_pass(plain_text_pwd):
    """
    Encrypt a plain text password.

    In order to avoid exposure of plain text password in the code, this
    helper function can be used to store hashed password directly usable for
    the elog connection.

    Parameters
    ----------
    plain_text_pwd : string
        The plain text password as introduced by the user to be encrypted.

    Returns
    -------
    string
        The hashed password to be used directly in the elog connect method.

    """
    return elog.logbook._handle_pswd(plain_text_pwd, True)


def dump_yaml_file(yaml_dict, yaml_filename):
    """
    Dump a yaml dictionary to a file.

    This helper function allows to save a yaml dictionary in a file using the
    right encoding.
    A line of comment is prepended to the file.

    Parameters
    ----------
    yaml_dict : dict
        The dictionary to be dumped on file.
    yaml_filename : str or path-like
        The output filename of the yaml dump..

    Returns
    -------
    None.

    """
    with open(yaml_filename, 'w', encoding='utf-8') as f:
        f.write(
            f'# YAML FILE Dumped at {datetime.now():%Y-%m-%d %H:%M:%S}\n\n')
        yaml.dump(yaml_dict, f, allow_unicode=True)


class ResolutionUnit(IntEnum):
    """Resolution unit of a TIFF file."""

    NONE = 1
    INCH = 2
    CM = 3

    @staticmethod
    def inverse_resolution_unit(cls):
        """Return the inverse resolution unit."""
        if cls.name == 'NONE':
            return 'none'
        elif cls.name == 'INCH':
            return 'dpi'
        elif cls.name == 'CM':
            return 'dpcm'

    def __str__(self):
        """.Return the string value."""
        return self.name


class ResolutionSource(IntEnum):
    """Enumerator used to define from where the resolution information should be taken."""

    TIFF_TAG = auto()
    FEI_TAG = auto()


class PictureResolution:
    """
    Picture Resolution class.

    It contains the horizontal and vertical resolution of a microscope picture
    along with the unit of measurements

    """

    def __init__(self, xres, yres, ures):
        if xres <= 0 or yres <= 0:
            raise ValueError('Resolution must be positive')
        self.xres = float(xres)
        self.yres = float(yres)
        if isinstance(ures, ResolutionUnit):
            ures = ResolutionUnit(ures)
        if ures not in (ResolutionUnit.NONE, ResolutionUnit.INCH, ResolutionUnit.CM):
            raise autoerror.WrongResolutionUnit('Invalid resolution unit')
        self.ures = ures

    def __eq__(self, other):
        """
        Compare two Picture Resolution object.

        If the second object has the same unit of measurements of the first one,
        the comparison is made straight forward looking at the horizontal and
        vertical resolution.

        If the two have different unit of measurements, then the second is
        temporary converted and the two resolution values are then compared.

        For the comparison a rounding of 5 digits is used.

        Parameters
        ----------
        other : PictureResolution instance
            Another picture resolution instance

        Returns
        -------
        bool
            True if the two PictureResolution objects are identical or at
            least equivalent. False otherwise.

        """
        if self.ures == other.ures:
            return round(self.xres, 5) == round(other.xres, 5) and round(self.yres, 5) == round(other.yres, 5)
        else:
            old_ures = other.ures
            other.convert_to_unit(self.ures)
            is_equal = round(self.xres, 5) == round(other.xres, 5) and round(
                self.yres, 5) == round(other.yres, 5)
            other.convert_to_unit(old_ures)
            return is_equal

    def __str__(self):
        """Print out a Picture Resolution instance."""
        return (f'({self.xres:.5} {ResolutionUnit.inverse_resolution_unit[self.ures]} '
                f'x {self.yres:5} {ResolutionUnit.inverse_resolution_unit[self.ures]})')

    def __repr__(self):
        """Represent a Picture_resolution."""
        return f'{self.__class__.__name__}(self.xres, self.yres, self.ures)'

    def as_tuple(self):
        """Return the picture resolution as a tuple."""
        return self.xres, self.yres, self.ures

    def convert_to_unit(self, desired_um):
        """
        Convert the Picture Resolution to the desired unit of measurement.

        Parameters
        ----------
        desired_um : ResolutionUnit
            The target resolution unit

        Raises
        ------
        autoerror.WrongResolutionUnit
            If an invalid target resolution unit is passed.

        autoerror.ImpossibleToConvert
            If one of the two resolution has ResolutionUnit.NONE

        Returns
        -------
        None.

        """
        if self.ures == ResolutionUnit.NONE or desired_um == ResolutionUnit.NONE:
            raise autoerror.ImpossibleToConvert(
                'Impossible to convert, because resolution unit of measurement is none.')

        if self.ures == desired_um:
            conv_fact = 1
        else:
            if self.ures == ResolutionUnit.INCH:
                if desired_um == ResolutionUnit.CM:
                    conv_fact = 1 / 2.54
                else:
                    raise autoerror.WrongResolutionUnit(
                        'Invalid resolution unit of measurement')
            else:  # self.ures == ResolutionUnit.cm
                if desired_um == ResolutionUnit.INCH:
                    conv_fact = 2.54
                else:
                    raise autoerror.WrongResolutionUnit(
                        'Invalid resolution unit of measurement')

        self.ures = desired_um
        self.xres *= conv_fact
        self.yres *= conv_fact


def get_picture_resolution(tiffinfo: PIL.TiffImagePlugin.ImageFileDirectory_v2,
                           source: ResolutionSource = ResolutionSource.TIFF_TAG,
                           desired_um: ResolutionUnit = None) -> PictureResolution | None:
    """
    Get the Picture Resolution object from TIFF tags.

    All TIFF images must have the resolution information store in the TIFF tags.
    In the case of FEI images, the resolution information stored in the basic
    TIFF tags is incorrect while the correct one is saved in the custom FEI
    tags.

    Using this method, both resolution information can be retrieved using the
    ResolutionSource enumerator.

    Using the desired_um, the Picture Resolution can be converted to a convenient
    unit of measurements

    Parameters
    ----------
    tiffinfo : PIL.TiffImagePlugin.ImageFileDirectory_v2
        A dictionary containing all TIFF tags
    source : ResolutionSource, optional
        From where the resolution information should be taken from.
        Possible values are 'FEI_TAG' and 'TIFF_TAG'.
        The default is 'TIFF_TAG'.
    desired_um : ResolutionUnit, optional
        The resolution unit in which the Picture resolution should be returned.
        Use None to obtain the original one without conversion.
        The default is None.

    Returns
    -------
    PictureResolution :
        The picture resolution. None if it was not possible to calculate it.

    """
    if not isinstance(tiffinfo, ImageFileDirectory_v2):
        raise TypeError(
            'tiffinfo must be a PIL.TiffImagePlugin.ImageFileDirectory_v2')

    if isinstance(source, (ResolutionSource, str)):
        if isinstance(source, str):
            try:
                source = ResolutionSource(source)
            except ValueError as e:
                log.error('Unknown source of resolution')
                log.exception(e)
                raise e
    else:
        raise TypeError(
            'Wrong type for source. Please use ResolutionSource enumerator.')

    if desired_um not in (ResolutionUnit.NONE, ResolutionUnit.INCH, ResolutionUnit.CM):
        raise ValueError('Invalid value for the target unit of measurement')

    resolution = None

    if source == ResolutionSource.TIFF_TAG:
        xres_code = 282
        yres_code = 283
        ures_code = 296

        resolution = PictureResolution(tiffinfo.get(
            xres_code), tiffinfo.get(yres_code), ResolutionUnit(tiffinfo.get(ures_code)))
        if desired_um is not None:
            resolution.convert_to_unit(desired_um)

    elif source == ResolutionSource.FEI_TAG:

        fei_tag_code = 34682
        fei_metadata = configparser.ConfigParser(allow_no_value=True)
        fei_metadata.read_string(tiffinfo[fei_tag_code])

        pixel_width = fei_metadata.getfloat('Scan', 'PixelWidth')
        pixel_height = fei_metadata.getfloat('Scan', 'PixelHeight')

        xres = 1 / (pixel_width * 100)
        yres = 1 / (pixel_height * 100)
        ures = ResolutionUnit.CM

        resolution = PictureResolution(xres, yres, ures)
        if desired_um is not None:
            resolution.convert_to_unit(desired_um)

    return resolution


class UserRole(IntEnum):
    """Enumerator to define user role for the data model.

    The actual value of each role is irrelevant, it is only important that each
    element stays constant during on single execution and that their value is
    greater than QtCore.Qt.UserRole + 1.

    It is a perfect application case for an IntEnum with auto() values and
    overloaded _generate_next_value_.


    """

    # noinspection PyProtectedMember
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> int:
        """
        Generate the next value.

        This function is called every time a new element with auto() is added.
        The user role must be at least QtCore.Qt.UserRole + 1.

        Parameters
        ----------
        name : string
            The name of the enum element.
        start : int
            The value of the first enumerator. It is always 1.
        count : int
            The number of enumerator values so far.
        last_values : iterable
            A list of all already used values.

        Returns
        -------
        int
            The next value starting from QtCore.Qt.UserRole+1

        """
        return IntEnum._generate_next_value_(name, QtCore.Qt.UserRole + 1, count, last_values)

    ITEM_TYPE = auto()
    DESCRIPTION = auto()
    EXTRA = auto()
    IMAGE = auto()
    PIC_ID = auto()
    CAPTION = auto()
    SAMPLE_FULL_NAME = auto()
    SAMPLE_LAST_NAME = auto()
    ATTACHMENT_PATH = auto()
    ATTACHMENT_FILE = auto()


class ElementType(Enum):
    """Enumerator to define the various type of items."""

    TEXT = 'Text'
    SECTION = 'Section'
    SAMPLE = 'Sample'
    NAVIGATION_PIC = 'NavPic'
    MICROSCOPE_PIC = 'MicroPic'
    ATTACHMENT_FILE = 'AttachmentFile'
    YAML_FILE = 'YAMLFile'


class PictureType(Enum):
    """Enumerator to define the various microscope picture types."""

    GENERIC_MICROSCOPE_PICTURE = 'Generic'
    FEI_MICROSCOPE_PICTURE = 'FEI'
    QUATTRO_MICROSCOPE_PICTURE = 'FEI.Quattro'
    VERSA_MICROSCOPE_PICTURE = 'FEI.Versa'

    def __str__(self):
        """
        Convert to string.

        Returns
        -------
        str
            the enumerator member value as a string

        """
        return self.value


class ReadOnlyDecision(IntEnum):
    """Enumerator defining the user choice in case of a read-only entry.

    When the user is attempting to write/edit/delete a read-only entry in the logbook
    he is asked to take a decision on what he would like to do.

    Overwrite: the edit-lock is switched off and the read-only entry is turned editable.

    Backup: the read-only entry is backed up in another entry with the same content but
        where the protocol number has been edited inserting a backup tag.

    Edit: the user has the possibility to modify the protocol number of the current entry
        hopefully not corresponding to another read-only entry.

    """

    Overwrite = auto()
    Backup = auto()
    Edit = auto()


class LoggerDecision(Enum):
    """Enumerator for the user decision about the newly added log level."""

    KEEP = 'keep'
    KEEP_WARN = 'keep-warn'
    OVERWRITE = 'overwrite'
    OVERWRITE_WARN = 'overwrite-warn'
    RAISE = 'raise'


def add_logging_level(level_name, level_num, method_name=None, if_exists=LoggerDecision.KEEP, *,  # noqa: C901
                      exc_info=False, stack_info=False):
    """Add a logging level."""

    def for_logger_class(self, message, *args, **kwargs):
        """
        No idea!

        Parameters
        ----------
        self
        message
        args
        kwargs
        """
        if self.isEnabledFor(level_num):
            kwargs.setdefault('exc_info', exc_info)
            kwargs.setdefault('stack_info', stack_info)
            self._log(level_num, message, args, **kwargs)

    def for_logging_module(*args, **kwargs):
        """
        No idea.

        Parameters
        ----------
        args
        kwargs
        """
        kwargs.setdefault('exc_info', exc_info)
        kwargs.setdefault('stack_info', stack_info)
        logging.log(level_num, *args, **kwargs)

    if not method_name:
        method_name = level_name.lower()

    items_found = 0
    items_conflict = 0

    logging._acquireLock()
    try:
        registered_num = logging.getLevelName(level_name)
        logger_class = logging.getLoggerClass()

        if registered_num != 'Level ' + level_name:
            items_found += 1
            if registered_num != level_num:
                if if_exists == LoggerDecision.RAISE:
                    # Technically this is not an attribute issue, but for
                    # consistency
                    raise AttributeError(
                        'Level {!r} already registered in logging '
                        'module'.format(level_name)
                    )
                items_conflict += 1

        if hasattr(logging, level_name):
            items_found += 1
            if getattr(logging, level_name) != level_num:
                if if_exists == LoggerDecision.RAISE:
                    raise AttributeError(
                        'Level {!r} already defined in logging '
                        'module'.format(level_name)
                    )
                items_conflict += 1

        if hasattr(logging, method_name):
            items_found += 1
            logging_method = getattr(logging, method_name)
            if not callable(logging_method) or \
                    getattr(logging_method, '_original_name', None) != \
                    for_logging_module.__name__:
                if if_exists == LoggerDecision.RAISE:
                    raise AttributeError(
                        'Function {!r} already defined in logging '
                        'module'.format(method_name)
                    )
                items_conflict += 1

        if hasattr(logger_class, method_name):
            items_found += 1
            logger_method = getattr(logger_class, method_name)
            if not callable(logger_method) or \
                    getattr(logger_method, '_original_name', None) != \
                    for_logger_class.__name__:
                if if_exists == LoggerDecision.RAISE:
                    raise AttributeError(
                        'Method {!r} already defined in logger '
                        'class'.format(method_name)
                    )
                items_conflict += 1

        if items_found > 0:
            # items_found >= items_conflict always
            if (items_conflict or items_found < 4) and \
                    if_exists in (LoggerDecision.KEEP_WARN, LoggerDecision.OVERWRITE_WARN):
                action = 'Keeping' if if_exists == LoggerDecision.KEEP_WARN else 'Overwriting'
                if items_conflict:
                    problem = 'has conflicting definition'
                    items = items_conflict
                else:
                    problem = 'is partially configured'
                    items = items_found
                log.warning(
                    'Logging level {!r} {} already ({}/4 items): {}'.format(
                        level_name, problem, items, action)
                )

            if if_exists in (LoggerDecision.KEEP, LoggerDecision.KEEP_WARN):
                return

        # Make sure the method names are set to sensible values, but
        # preserve the names of the old methods for future verification.
        for_logger_class._original_name = for_logger_class.__name__
        for_logger_class.__name__ = method_name
        for_logging_module._original_name = for_logging_module.__name__
        for_logging_module.__name__ = method_name

        # Actually add the new level
        logging.addLevelName(level_num, level_name)
        setattr(logging, level_name, level_num)
        setattr(logger_class, method_name, for_logger_class)
        setattr(logging, method_name, for_logging_module)
    finally:
        logging._releaseLock()


class ElementTypeGuesser:
    """Helper class to guess the type of element starting from the filename."""

    def __init__(self, matching_patterns, exclude_patterns=None):
        """
        Build a ElementTypeGuesser.

        Parameters
        ----------
        matching_patterns : str, re.Pattern, list<str>
            A regular expression pattern for matching.
        exclude_patterns : str, re.Pattern, list<str>
            A regular expression pattern for exclusion.
            Set to None, to disable. The default is None.

        Returns
        -------
        None.

        """
        # check the input args
        if not isinstance(matching_patterns, (re.Pattern, str, list)):
            raise TypeError(
                'matching_patterns must be a re.Pattern, a string or a list of string.')

        if exclude_patterns is not None:
            if not isinstance(exclude_patterns, (re.Pattern, str, list)):
                raise TypeError(
                    'exclude_patterns must be a re.Pattern, a string or a list of string.')

        # check the matching_patterns. this must be either a re.Pattern
        if not isinstance(matching_patterns, re.Pattern):
            if isinstance(matching_patterns, str):
                self.matching_patterns = re.compile(matching_patterns)
            if isinstance(matching_patterns, list):
                self.matching_patterns = re.compile(
                    '|'.join(matching_patterns))

        # check the exclude_patterns. this must be either a re.Pattern
        if exclude_patterns is not None:
            if not isinstance(exclude_patterns, re.Pattern):
                if isinstance(exclude_patterns, str):
                    self.exclude_patterns = re.compile(exclude_patterns)
                if isinstance(exclude_patterns, list):
                    self.exclude_patterns = re.compile(
                        '|'.join(exclude_patterns))
        else:
            self.exclude_patterns = None

    def _is_matching(self, element_path):

        if isinstance(element_path, Path):
            self.element_path = str(element_path)
        elif isinstance(element_path, str):
            self.element_path = element_path
        else:
            raise TypeError('element_path must be either str or Path')

        return self.matching_patterns.search(element_path)

    def _is_excluded(self, element_path):
        if self.exclude_patterns is None:
            return False
        if isinstance(element_path, Path):
            self.element_path = str(element_path)
        elif isinstance(element_path, str):
            self.element_path = element_path
        else:
            raise TypeError('element_path must be either str or Path')

        return self.exclude_patterns.search(element_path)

    def is_ok(self, element_path):
        """
        Check if the element_path is ok.

        A path is ok if it machtes the matching pattern and if it is not
        excluded by the exclude pattern.

        Parameters
        ----------
        element_path : str | Path
            The path to be checked.

        Returns
        -------
        bool
            True if the element path is valid.

        """
        return self._is_matching(element_path) and not self._is_excluded(element_path)


def pretty_filesize(size_bytes):
    """
    Return a nicely formatted string with the filesize with the proper unit.

    Parameters
    ----------
    size_bytes : int
        This is the file size in bytes. Typically this is what is returned
        by Path().stat().st_size.

    Returns
    -------
    size : str
        Nicely formatted string representing the file size with the most
        appropriate unit of measurement.

    """
    if size_bytes == 0:
        return '0 B'
    size_name = ('B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    i = int(math.floor(math.log(size_bytes, 1924)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f'{s} {size_name[i]}'


class DateType(IntEnum):
    """Enumerator for selecting the type of date saved in the file."""

    ATIME = auto()
    MTIME = auto()
    CTIME = auto()


def get_date_from_file(file_stat: os.stat, date_type: DateType) -> datetime:
    """
    Return a datetime object with the file date.

    In the file_stat (as generated by Path.stat()) contains three different date
    information.

      - DateType.ATIME: last access time
      - DateType.MTIME: last modification time
      - DateType.CTIME: creation time

    The date information are stored as timestamp. This function is converting
    the timestamp in a datetime object in the local timezone.

    Parameters
    ----------
    file_stat : os.stat
        The os.stat information of the file under investigation.
    date_type : DateType
        A enumerator to select the type of date

    Returns
    -------
    local_datetime : datetime
        The date information as a datetime object in the local timezone.

    """
    if date_type == date_type.ATIME:
        ts = file_stat.st_atime
    elif date_type == date_type.MTIME:
        ts = file_stat.st_mtime
    elif date_type == date_type.CTIME:
        ts = file_stat.st_ctime
    else:  # should not happen
        ts = 0
    ts = datetime.fromtimestamp(ts, tz=timezone.utc)
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    utc = ts.replace(tzinfo=from_zone)
    cet = utc.astimezone(to_zone)

    return cet


def get_patterns_from_config() -> (list, list):
    """
    Get the patterns from the configuration module.

    This function is scanning the autoconfig module looking for variables whose name contains
    _MATCHING_PATTERNS or _EXCLUDE_PATTERNS.

    Those correspond to the variables used by the ElementTypeGuesser and they can potentially be used also for
    the event handler patterns.

    Returns
    -------
    matching_patterns, exclude_patterns : tuple(list)
        A 2-tuple with the two lists.

    """
    matching_patterns = []
    exclude_patterns = []
    for el in dir(autoconfig):
        if '_MATCHING_PATTERNS' in el and autoconfig.__getattr__(el) is not None:
            for pattern in autoconfig.__getattr__(el):
                matching_patterns.append(pattern)
        if '_EXCLUDE_PATTERNS' in el and autoconfig.__getattr__(el) is not None:
            for pattern in autoconfig.__getattr__(el):
                exclude_patterns.append(pattern)
    if len(matching_patterns) == 0:
        matching_patterns = None
    if len(exclude_patterns) == 0:
        exclude_patterns = None

    return matching_patterns, exclude_patterns


def reglob(path: str| Path, matching_regexes: str | list[str] | None, ignore_regexes: str | list[str] | None, recursive: bool = True) -> list[str]:
    """
    Emulates the glob.glob using regular expressions.

    Parameters
    ----------
    path: str | Path
        The root path from where the glob should be started.
    matching_regexes: str | list[str] | None
        One or several regular expressions to be used as matching patterns.
        Use None to get the equivalent of a '*' wildcard.
    ignore_regexes: str | list[str] | None
        One or several regular expressions to be used as excluding patterns.
        Use None to disable the exclusion mechanism.
    recursive: bool
        True if the search should be performed through all subdirectories.

    Returns
    -------
    list[str]:
        A list of all elements matching the regular expressions and not excluded.

    """
    if matching_regexes is None:
        matching_regexes = [r'.*']
    elif isinstance(matching_regexes, str):
        matching_regexes = [matching_regexes]

    if ignore_regexes is None:
        ignore_regexes = []
    elif isinstance(ignore_regexes, str):
        ignore_regexes = [ignore_regexes]

    matching_regexes = [re.compile(r) for r in matching_regexes]
    ignore_regexes = [re.compile(r) for r in ignore_regexes]

    file_list = []
    for file in glob.glob(path, recursive=recursive):
        if any(r.match(file) for r in ignore_regexes):
            pass
        elif any(r.match(file) for r in matching_regexes):
            file_list.append(file)

    return file_list
