import os.path
import sys
import subprocess
from time import sleep
from datetime import datetime
from systemd import journal as journalctl


def before_scenario(context, scenario):
    context.start_time = datetime.now()
    # Skip scenarios which require smoketest if it hasn't started yet
    if u'requires_smoketest' in scenario.effective_tags:
        if not os.path.isfile('/smoketest_passed'):
            sys.stdout.write("Skipping %s as smoketest failed\n" % scenario.name)
            scenario.skip()

    # Store initial abrt cli output to track new issues
    context.abrt_cli = subprocess.check_output("sudo abrt-cli ls", shell=True)

    # Use python-systemd to track messages in journal
    context.journal = journalctl.Reader()
    context.journal.log_level(journalctl.LOG_DEBUG)
    context.journal.this_boot()
    context.journal.seek_realtime(context.start_time)


def after_scenario(context, scenario):
    # Look for crashes since scenario start
    context.journal.flush_matches()
    context.journal.seek_realtime(context.start_time)
    context.journal.add_match(_AUDIT_TYPE='1701')
    match = context.journal.get_next()
    if match != {}:
        print(match)
        # Wait for abrt to get crash
        diff = ''
        for attempt in xrange(0, 30):
            new_abrt_cli = subprocess.check_output("sudo abrt-cli ls", shell=True)
            diff = new_abrt_cli[:len(context.abrt_cli)].strip().decode('utf8')
            if diff != '':
                context.embed('text/plain', diff, caption="ABRT")
                break
            sleep(1)

    # Add journal entries to the journal
    cmd = "sudo journalctl --no-pager -o short-monotonic -b --since='%s'" % context.start_time.strftime("%H:%M:%S")
    journal = subprocess.check_output(cmd, shell=True).decode('utf8')
    context.embed('text/plain', journal, caption="journal")

    context.journal.close()
