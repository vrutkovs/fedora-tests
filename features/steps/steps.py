from behave import step
from time import sleep
import subprocess
import os
from systemd import journal as journalctl


@step(u'Start {service_name} service')
def start_systemd_service(context, service_name):
    cmd = "sudo systemctl stop %s && sudo systemctl start %s" % (service_name, service_name)
    try:
        print("Running '%s'" % cmd)
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e


@step(u'Wait for process "{process}" to appear')
@step(u'Wait for process "{process}" to appear in {timeout} seconds')
def wait_for_process_to_appear(context, process, timeout=60):
    cmd = "pgrep %s" % process
    for attempt in xrange(0, timeout):
        try:
            print("Running '%s'" % cmd)
            out = subprocess.check_output(cmd, shell=True)
            if out != '':
                return
        except subprocess.CalledProcessError as e:
            print(e.output)
        sleep(1)
    raise Exception("Process %s didn't show up in %s secs" % (process, timeout))


@step(u'Wait for "{message_part}" message in journalctl')
@step(u'Wait for "{message_part}" message in journalctl in {timeout} seconds')
def wait_for_journalctl_message(context, message_part, timeout=60):
    journal = journalctl.Reader()
    try:
        journal.this_boot()
        journal.log_level(journalctl.LOG_DEBUG)
        journal.seek_realtime(context.seconds_since_epoch)
        journal.add_match(MESSAGE=message_part)
        for attempt in xrange(0, timeout):
            if journal.get_next() != {}:
                journal.close()
                return
            sleep(1)
        raise Exception("Message '%s' was not found in %s secs" % (message_part, timeout))
    finally:
        journal.close()


@step(u'Make sure "{group_name}" package group is installed')
def install_package_group(context, group_name):
    cmd = "sudo dnf groupinstall -y %s" % group_name
    try:
        print("Running '%s'" % cmd)
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e


@step(u'Touch "/smoketest_passed" file')
def touch_smoketest_passed(context):
    cmd = "sudo touch /smoketest_passed"
    try:
        print("Running '%s'" % cmd)
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e


@step(u'Run installed tests for "{prefix}" from "{package}"')
def run_installed_test_for_package(context, prefix, package):
    cmd = "sudo dnf install -y %s" % package
    try:
        print("Running '%s'" % cmd)
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e

    testout = '/tmp/testout.log'

    cmd = 'gnome-desktop-testing-runner %s/ --parallel 0 --status=yes &> %s' % (prefix, testout)
    try:
        if os.path.isfile(testout):
            os.remove(testout)
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        raise e
    finally:
        if os.path.isfile(testout):
            logfile = open(testout, 'r').read().decode('utf8')
            context.embed('text/plain', logfile, caption="Test output")
