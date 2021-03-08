import Tests
import HtmlTestRunner
import os
import time
import unittest
from libs import builtins

SUITE = unittest.TestSuite()
SKIP = []

direct = os.getcwd()

def load_suite(base_path, root_dir="/.."):
    global SUITE
    global SKIP
    from importlib.machinery import SourceFileLoader
    testcase = SourceFileLoader("", base_path).load_module()
    for p, v in vars(testcase).items():
        if type(v) == type.__class__:
            test = eval("testcase.{}".format(p))
            if test not in SKIP:
                SUITE.addTests([
                    unittest.defaultTestLoader.loadTestsFromTestCase(test),
                ])
                SKIP.append(test)
            else:
                pass

def run():
    global SUITE
    runner = HtmlTestRunner.HTMLTestRunner(
            #stream=fw,
            verbosity= builtins.VERBOSITY_LEVEL,
            report_title='Test Report',
            descriptions='Smoke Tests',
            combine_reports=True
    )
    runner.run(SUITE)

if __name__ == '__main__':
    unittest.main()