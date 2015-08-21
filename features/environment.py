import os.path
import sys


def before_scenario(context, scenario):
    if u'requires_smoketest' in scenario.effective_tags:
        if not os.path.isfile('/smoketest_passed'):
            sys.stdout.write("Skipping %s as smoketest failed\n" % scenario.name)
            scenario.skip()
