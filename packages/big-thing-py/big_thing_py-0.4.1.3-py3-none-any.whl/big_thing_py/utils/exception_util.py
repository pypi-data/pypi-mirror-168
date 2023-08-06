from common import *
from utils import *

import traceback


def print_error(e: Exception):
    traceback_msg = traceback.format_exc()
    SOPLOG_DEBUG(f'Traceback message : {traceback_msg}\nError: {e}', 'red')
