import os
import logging

logging.basicConfig(level=logging.INFO)


def get_app_directory():
    return os.path.split(__file__)[0]
