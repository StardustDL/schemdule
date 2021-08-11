import logging
import os

import click

import enlighten

__version__ = "0.0.9"


def get_app_directory():
    return os.path.split(__file__)[0]
