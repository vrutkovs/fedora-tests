from behave import step
from time import sleep
import subprocess


@step(u'Start {service_name} service')
def start_systemd_service(context, service_name):
    cmd = "sudo systemctl stop %s && sudo systemctl start %s" % (service_name, service_name)
    try:
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
    cmd = "sudo journalctl --no-pager -o short-monotonic -q -b | grep '%s'" % message_part
    for attempt in xrange(0, timeout):
        try:
            out = subprocess.check_output(cmd, shell=True)
            if out != '':
                return
        except subprocess.CalledProcessError as e:
            print(e.output)
        sleep(1)
    raise Exception("Message '%s' was not found in %s secs" % (message_part, timeout))


@step(u'Make sure "{group_name}" package group is installed')
def install_package_group(context, group_name):
    try:
        subprocess.check_output("sudo dnf groupinstall -y %s" % group_name, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e