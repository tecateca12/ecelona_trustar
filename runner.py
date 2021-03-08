'''
This file is a placeholder for tcrunner functionality stored in the tcrunner library.
'''

from libs.runner_library import main as tc_main
import sys, os, inspect
from libs import builtins

if __name__ == "__main__":
    # add builtins to __builtins__
    __builtins__.builtins = builtins
    tc_main()
