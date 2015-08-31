from behave import step
from time import sleep
from gi.repository import Gio
from gi.repository import GLib
import subprocess
import os
import json


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
    cmd = "sudo systemctl start %s" % service_name
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
        subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
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
    # Check that app is in the list
    _appListUnfiltered = Gio.AppInfo.get_all()
    _appList = []
    for app in _appListUnfiltered:
        if app.get_nodisplay():
            continue
        if app.has_key('Categories') and \
           'X-GNOME-Settings-Panel' in app.get_string('Categories'):
            continue
        _appList.append(app)

    matchedApps = list(filter(lambda x: x.get_name() == appname, _appList))
    if len(matchedApps) == 0:
        raise Exception("Cannot find '%s' app" % appname)

    app_obj = matchedApps[0]

    sessionBus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    _shell = Gio.DBusProxy.new_sync(sessionBus, 0, None,
                                    "org.gnome.Shell", "/org/gnome/Shell",
                                    "org.gnome.Shell", None)

    # Close all apps
    code = 'Shell.AppSystem.get_default().get_running().forEach(function (app) { app.request_quit(); });'
    [success, result] = _shell.call_sync("Eval", GLib.Variant("(s)", (code,)), 0, -1, None)
    if not success:
        raise Exception("Failed to eval '%s': %s" % (code[0:20], result))

    app_obj.launch([], None)

    # Wait for app to appear in a list of running apps
    test_result = False
    for attempt in xrange(0, 30):
        sleep(1)
        runningApps = []
        code = 'Shell.AppSystem.get_default().get_running().map(function (a) { return a.get_id(); });'
        [success, result] = _shell.call_sync("Eval", GLib.Variant("(s)", (code,)), 0, -1, None)
        if not success:
            raise Exception("Failed to eval '%s': %s" % (code[0:20], result))
        if result:
            runningApps = json.loads(result)

        if app_obj.get_id() in runningApps:
            test_result = True
            context.execute_steps(u'* Make screenshot')
            break

    # Close all apps
    code = 'Shell.AppSystem.get_default().get_running().forEach(function (app) { app.request_quit(); });'
    [success, result] = _shell.call_sync("Eval", GLib.Variant("(s)", (code,)), 0, -1, None)
    if not success:
        raise Exception("Failed to eval '%s': %s" % (code[0:20], result))

    if not test_result:
        raise Exception("App %s didn't start" % appname)
