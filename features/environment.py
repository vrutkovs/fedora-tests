import os.path
import sys
import subprocess
from time import sleep


def before_scenario(context, scenario):
    if u'requires_smoketest' in scenario.effective_tags:
        if not os.path.isfile('/smoketest_passed'):
            sys.stdout.write("Skipping %s as smoketest failed\n" % scenario.name)
            scenario.skip()


def after_tag(context, tag):
    if tag == 'stop_gdm':
        # Stop gdm and make sure its dead after scenario
        cmd = "pgrep gnome-session"
        for attempt in xrange(0, 30):
            try:
                out = subprocess.check_output(cmd, shell=True)
                if out != '':
                    cmd = "killall gnome-session && sudo systemctl stop gdm"
                    try:
                        subprocess.check_output(cmd, shell=True)
                    except subprocess.CalledProcessError as e:
                        print(e.output)
                else:
                    return
            except subprocess.CalledProcessError as e:
                print(e.output)
            sleep(5)
