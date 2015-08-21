import os.path
import sys


def before_scenario(context, scenario):
    if scenario.tag == 'requires_smoketest':
        if not os.path.isfile('/smoketest_passed'):
            sys.stdout.write("Skipping %s as smoketest failed\n" % scenario.name)
            scenario.skip()
