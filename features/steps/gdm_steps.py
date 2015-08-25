from behave import step

import ConfigParser
import subprocess
import os
from sys import exit
from time import sleep

GDM_CONFIG_FILE = '/etc/gdm/custom.conf'


@step(u'Set gdm to use "{session_name}" session')
def set_gdm_to_use_session(context, session_name):
    cmd = "sudo dbus-send --print-reply --reply-timeout=60000 --system --type=method_call --print-reply "
    cmd += "--dest=org.freedesktop.Accounts /org/freedesktop/Accounts/User1000 "
    cmd += "org.freedesktop.Accounts.User.SetXSession string:%s" % session_name
    try:
        print("Running '%s'" % cmd)
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e


@step(u'Set gdm options')
def set_gdm_options(context):
    config = ConfigParser.ConfigParser()
    config.optionxform = str

    for row in context.table:
        if not config.has_section(row['section']):
            config.add_section(row['section'])
        config.set(row['section'], row['key'], row['value'])

    tmppath = '/tmp/gdm.config'
    with open(tmppath, 'wb') as configfile:
        config.write(configfile)

    cmd = "sudo cp %s %s" % (tmppath, GDM_CONFIG_FILE)
    try:
        print("Running '%s'" % cmd)
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e


@step(u'Start gdm for "{username}" user and "{session}" session')
def start_gdm(context, username, session):
    context.execute_steps(u"""
        * Set gdm options:
            | section | key                  | value |
            | daemon  | AutomaticLogin       | %s    |
            | daemon  | AutomaticLoginEnable | true  |
            | debug   | Enable               | true  |
        * Set gdm to use "%s" session
    """ % (username, session))
    exception = None
    for attempt in xrange(0, 3):
        try:
            context.execute_steps(u"""
                * Start gdm service (without restarting it)
                * Wait for process "gdm" to appear
                * Wait for process "gnome-session" to appear
                * Wait for GNOME Shell to startup
            """)
            exception = None
            break
        except Exception as e:
            exception = e

    if exception:
        raise exception
    set_env_vars()


def set_env_vars():
    process = subprocess.Popen("pgrep -u test gnome-session", shell=True, stdout=subprocess.PIPE)
    session_id = process.communicate()[0].strip('\n')

    if not session_id:
        print("Can't find gnome-session id, trying gnome-shell")
        process = subprocess.Popen("pgrep -u test gnome-shell", shell=True, stdout=subprocess.PIPE)
        session_id = process.communicate()[0].strip()

    if not session_id:
        print("No session pid found, exiting")
        exit(1)

    process = subprocess.Popen("cat /proc/%s/environ" % session_id, shell=True, stdout=subprocess.PIPE)
    environ = process.communicate()[0]
    environs = environ.replace('\x00', '\n').strip().split('\n')

    for var in ['DISPLAY', 'XAUTHORITY', 'DBUS_SESSION_BUS_ADDRESS', 'WAYLAND_DISPLAY']:
        for env in environs:
            if '%s=' % var in env:
                os.environ[var] = env.replace('%s=' % var, '')

    gdm_session = None
    for env in environs:
        if 'GDMSESSION=' in env:
            gdm_session = env.replace('GDMSESSION=', '')

    if gdm_session and 'wayland' in gdm_session:
        print("Wayland session detected")
        os.environ['GDK_BACKEND'] = 'wayland'

    # Get some more debugging output
    os.environ['G_MESSAGES_DEBUG'] = 'all'

    if 'WAYLAND_DISPLAY' not in os.environ:
        os.environ['WAYLAND_DISPLAY'] = 'wayland-0'


@step(u'Make screenshot')
def make_screenshot(context, name="screenshot"):
    set_env_vars()
    my_env = os.environ.copy()
    screenshot_path = "/tmp/%s.jpg" % name
    process = subprocess.Popen(
        "gnome-screenshot -p -f %s" % screenshot_path,
        shell=True, stdout=subprocess.PIPE, env=my_env)
    process.communicate()[0]
    sleep(5)

    if os.path.isfile(screenshot_path):
        print("Screenshot saved to %s" % screenshot_path)
        context.embed('image/jpg', open(screenshot_path, 'r').read(), caption="Screenshot")
