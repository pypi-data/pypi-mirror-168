from configparser import ConfigParser, MissingSectionHeaderError

import pytest

from autologbook.autoerror import NotAValidConfigurationFile
from autologbook.autotools import generate_default_conf, safe_configread


def test_generate_default_conf():
    config = generate_default_conf()
    assert isinstance(config, ConfigParser)


def test_safe_configread():

    default_config = generate_default_conf()

    with pytest.raises(TypeError):
        # reading a file without name (None)
        safe_configread(conffile=None)

    with pytest.raises(MissingSectionHeaderError):
        # reading an invalid file
        safe_configread(__file__)

    # write an empty configuration file
    empty_config = ConfigParser()
    empty_config_filename = 'empty_config.ini'
    empty_config.write(empty_config_filename)

    # safe_read the empty configuration file
    with pytest.raises(NotAValidConfigurationFile):
        read_config = safe_configread(empty_config_filename)
