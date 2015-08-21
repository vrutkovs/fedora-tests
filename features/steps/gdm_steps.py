from behave import step

import ConfigParser
import tempfile
import subprocess

GDM_CONFIG_FILE = '/etc/gdm/custom.conf'


@step(u'Set gdm to use "{session_name}" session')
def set_gdm_to_use_session(context, session_name):
    cmd = "dbus-send --print-reply --reply-timeout=60000 --system --type=method_call --print-reply "
    cmd += "--dest=org.freedesktop.Accounts /org/freedesktop/Accounts/User1000 "
    cmd += "org.freedesktop.Accounts.User.SetXSession string:%s" % session_name
    try:
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e


@step(u'Set gdm options')
def set_gdm_options(context):
    config = ConfigParser.ConfigParser()

    for row in context.table:
        if not config.has_section(row['section']):
            config.add_section(row['section'])
        config.set(row['section'], row['key'], row['value'])

    tmppath = '/tmp/gdm.config'
    with open(tmppath, 'wb') as configfile:
        config.write(configfile)

    cmd = "sudo cp %s %s" % (tmppath, GDM_CONFIG_FILE)
    try:
        subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e
