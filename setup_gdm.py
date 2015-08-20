import sys
import os
import subprocess

session_type = 'gnome'
login_type = 'Timed'

if len(sys.argv) > 1:
    session_type = sys.argv[1]

if len(sys.argv) > 2:
    login_type = sys.argv[2]

print("Session: '%s', login type: '%s'" % (session_type, login_type))

with open("/etc/gdm/custom.conf", 'w') as f:
    f.write("[daemon]\n")
    f.write("%sLogin=test\n" % login_type)
    f.write("%sLoginEnable=true\n" % login_type)
    if login_type == 'Timed':
        f.write("TimedLoginDelay=10\n")
    f.write("\n")
    f.write("[debug]\n")
    f.write("Enable=true\n")

template = "dbus-send --print-reply --reply-timeout=60000 --system --type=method_call --print-reply --dest=org.freedesktop.Accounts /org/freedesktop/Accounts%s"

command = template % " org.freedesktop.Accounts.CreateUser string:'test' string: int32:0"
print("Running '%s'" % command)
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
print("Output: %s" % process.communicate()[0])

command = template % "/User1000 org.freedesktop.Accounts.User.SetPassword string:'' string:''"
print("Running '%s'" % command)
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
print("Output: %s" % process.communicate()[0])

command1 = "/User1000 org.freedesktop.Accounts.User.SetXSession string:%s" % session_type
command = template % command1
print("Running '%s'" % command)
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
print("Output: %s" % process.communicate()[0])

command = template % " org.freedesktop.Accounts.CacheUser string:'test'"
print("Running '%s'" % command)
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
print("Output: %s" % process.communicate()[0])

print("Restarting gdm")
os.system("systemctl restart gdm")
