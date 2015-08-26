from behave import step
from time import sleep
import subprocess
import os


@step(u'Start {service_name} service')
def start_systemd_service(context, service_name):
    cmd = "sudo systemctl stop %s && sudo systemctl start %s" % (service_name, service_name)
    try:
        print("Running '%s'" % cmd)
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e


@step(u'Start {service_name} service (don\'t restart if started already)')
def start_systemd_service_unless_started(context, service_name):
    cmd = "sudo systemctl start %s" % (service_name, service_name)
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
    context.journal.flush_matches()
    context.journal.add_match(MESSAGE=message_part)
    for attempt in xrange(0, timeout):
        if context.journal.get_next() != {}:
            return
        sleep(1)
    raise Exception("Message '%s' was not found in %s secs" % (message_part, timeout))


@step(u'Wait for GNOME Shell to startup')
@step(u'Wait for GNOME Shell to startup in {timeout} seconds')
def wait_for_gnome_shell(context, timeout=60):
    context.journal.flush_matches()
    context.journal.add_match(MESSAGE_ID="f3ea493c22934e26811cd62abe8e203a")
    for attempt in xrange(0, timeout):
        if context.journal.get_next() != {}:
            return
        sleep(1)
    raise Exception("GNOME Shell start message was not found in %s secs" % timeout)


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


@step(u'Start "{appname}" application')
def start_app(context, appname):
    raise NotImplementedError(u'STEP: Given Start "org.gnome.Nautilus" application')


@step(u'Stop "{appname}" application')
def stop_app(context):
    raise NotImplementedError(u'STEP: Given Stop "org.gnome.Nautilus" application')
