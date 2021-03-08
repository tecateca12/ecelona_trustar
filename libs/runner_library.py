import sys
import os
import inspect
import shlex
import json
from libs.unittest_runner import load_suite
from libs.unittest_runner import run as custom_runner
from argparse import ArgumentParser, ArgumentTypeError
from argparse import RawDescriptionHelpFormatter
from libs import builtins, driver

__all__ = []
__version__ = 0.1
__date__ = '2021-03-03'
__updated__ = '2021-03-04'
PROFILE = 0


def get_features_from_path(testpath='Tests'):
    """ Retrns a list of all TESTCASE_TEMPLATE_NAME.py files within the
            given directory.
    """
    testdirs = []
    for base_dir, folders, files in os.walk(os.path.join(builtins.PROJECT_PATH, testpath)):
        testdirs.extend([os.path.join(base_dir, f) for f in files if f == 'testcase.py'])
    if testdirs == []:
        print("No test files found in the testdir: {testpath}")
    return testdirs

def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (
        program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Ezequiel Celona on %s.

   USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(
            description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-V', '--version', 
                            action='version',
                            version=program_version_message)
        parser.add_argument('-e', '--env', 
                            dest="env",
                            help="select the environment to run tests (dev, local)",
                            default=None)
        parser.add_argument('-b', '--browser', 
                            dest="browser",
                            help="select the browser to run tests (Chrome, Firefox. IE, Edge, Opera, Safari)", 
                            default=None)
        parser.add_argument("-f", "--filter",
                            dest="filt",
                            default=None,
                            action='append',
                            help='Tells lettuce to run the specified tags only; '
                            'can be used multiple times to define more tags'
                            '(prefixing tags with "-" will exclude them and '
                            'prefixing with "~" will match approximate words)')
        parser.add_argument(dest="paths",
                            help="paths to folder(s) with source file(s) [default: %(default)s]",
                            metavar="path",
                            default="Tests",
                            nargs='+')

        # Process arguments
        args = parser.parse_args()
        tags = None
        if args.filt:
            tags = [tag.strip('@') for tag in args.filt if tag != "None"]
            tags = tags if tags else None
        paths = args.paths
        env = args.env
        browser = args.browser

        # Try and load user defined config (tcrunner.json) file into builtins
        # If its not present it loads the default values
        try:
            with open("config.json", "r") as rh:
                config_file = json.load(rh)
        except IOError:
            # No custom local configuration is present
            raise ValueError("No custom local configuration is present")

        for def_value in config_file:
            setattr(builtins, def_value, config_file[def_value])

        # set environment
        if env is not None and env in builtins.URL_FOR_ENV.keys():
            builtins.ENVIRONMENT = env
        elif env is not None:
            builtins.ENVIRONMENT = "runtime"
            builtins.URL_FOR_ENV["runtime"] = env

        # set browser
        builtins.BROWSER = browser if browser is not None else builtins.BROWSER
        driver.init_browser(getattr(driver, builtins.BROWSER))

        # set up base url
        builtins.BASE_URL = builtins.URL_FOR_ENV[builtins.ENV]

        # set up Page Object functionality
        with open(os.path.join(os.path.abspath(os.getcwd()), "PO", 'po.json'), 'r') as f:
            builtins.PO = json.load(f)

        # move old results to history
        builtins.prepare_results()

        # Initial message
        if builtins.VERBOSITY_LEVEL > 0:
            print("Verbose mode on")
            if builtins.RECURSIVE:
                print("Recursive mode on")
            else:
                print("Recursive mode off")

        # Run tests
        result = []
        #scripts = []
        final_rc = 0
        for inpath in paths:
            if builtins.RECURSIVE:
                for testcase_file in get_features_from_path(inpath):
                    load_suite(testcase_file)
            else:
                pass
                #final_rc = int(run_test(inpath, tags))
                #result.append([inpath, final_rc])

        custom_runner()
        driver.quit_browser()


        # builtins.print_result(result)
        return 0 if not final_rc else 1
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


if __name__ == "__main__":
     sys.exit(main())
