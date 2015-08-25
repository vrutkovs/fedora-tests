import os.path
import sys
import subprocess
from time import sleep
from datetime import datetime
from systemd import journal as journalctl


def before_scenario(context, scenario):
    # Skip scenarios which require smoketest if it hasn't started yet
    if u'requires_smoketest' in scenario.effective_tags:
        if not os.path.isfile('/smoketest_passed'):
            sys.stdout.write("Skipping %s as smoketest failed\n" % scenario.name)
            scenario.skip()

    context.abrt_cli = subprocess.check_output("sudo abrt-cli ls", shell=True)
    context.start_time = datetime.now().strftime("%H:%M:%S")
    context.journal = journalctl.Reader()
    context.journal.log_level(journalctl.LOG_DEBUG)
    context.journal.this_boot()
    context.journal.seek_realtime(datetime.now())


def after_scenario(context, scenario):
    # Save abrt diff here
    new_abrt_cli = subprocess.check_output("sudo abrt-cli ls", shell=True)
    diff = new_abrt_cli[len(context.abrt_cli):].decode('utf8')
    if diff != '':
        context.embed('text/plain', diff, caption="ABRT")

    # Add journal entries to the journal
    cmd = "sudo journalctl --no-pager -o short-monotonic --since='%s'" % context.start_time
    journal = subprocess.check_output(cmd, shell=True).decode('utf8')
    context.embed('text/plain', journal, caption="journal")

    context.journal.close()


def after_tag(context, tag):
    if tag == 'stop_gdm':
        # Stop gdm and make sure its dead after scenario
        for attempt in xrange(0, 30):
            try:
                subprocess.check_output("pgrep gnome-session", shell=True)
                subprocess.check_output("killall gnome-session; sudo systemctl stop gdm", shell=True)
            except subprocess.CalledProcessError:
                break
            sleep(5)
