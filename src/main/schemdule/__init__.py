import os
import logging
import click
import enlighten


def get_app_directory():
    return os.path.split(__file__)[0]
