import os
import sys

PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, PATH + '/../')

from python_lambda_logging.lambda_logging import *

def test_lambda():
    pass