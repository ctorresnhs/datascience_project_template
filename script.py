# BASE IMPORTS AND UTILS
import sys,os
import pandas as pd
import numpy as np

from dslib import *

from config import Conf
cfg:Conf = Conf()

from dslib.utils import project_logger
project_logger = project_logger(project_name=cfg.params.project_name,file_log_path=cfg.paths.project_log)
info    = project_logger.get_info()
debug   = project_logger.get_debug()
timed_info = project_logger.timed_info      #decorator
timed_debug = project_logger.timed_debug    #decorator
#============================================================================================================
## UTILS

## SCRIPT
def main ():
    pass

if __name__ == '__main__':
    main()

